/* eslint-disable no-console */

// ~~~~~~~~~~~~~~~~~~~~ Imports ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

const prompts = require("prompts");
const { Builder } = require("selenium-webdriver");
const chrome = require("selenium-webdriver/chrome");
const looksSame = require("looks-same");
const fs = require("fs");
const glob = require("glob");
var yaml = require("js-yaml");
const cmdArg = process.argv[2];
const configFile = glob.sync("test/visual-regression-test/vrt_config.yml");
var imgLocations = "test/visual-regression-test/";

// check if config file argument is passed. create the file if it does not exist and quit all running processes
if (
  cmdArg === "config" &&
  (typeof configFile === "undefined" || configFile.length === 0)
) {
  fs.copyFileSync(
    "test/visual-regression-test/vrt_config_template.yml",
    "test/visual-regression-test/vrt_config.yml"
  );
  console.log(
    "New config file created @ vrt_config.yml. Edit the file and run the command again"
  );
  process.exit(0);
}

// ~~~~~~~~~~~~~~~~~~~~ Driver settings and options ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

// instantiate browser with options
const driver = new Builder()
  .forBrowser("chrome")
  .setChromeOptions(new chrome.Options().headless())
  .build();

// set window size while browser is open
const windowOptions = (w, h) => {
  return driver
    .manage()
    .window()
    .setSize(w, h);
};

// ~~~~~~~~~~~~~~~~~~~~ loader functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

// global for starting and stopping loader function and counter
let timerStart;
let timerCounter;

// loader function runs during entire process
function loader() {
  var P = ["   ", ".  ", ".. ", "..."];
  var x = 0;
  return setInterval(function() {
    process.stdout.write("\rLooking for regressions" + P[x++]);
    x %= 4;
  }, 250);
}

// called when no regressions are found or after generating diff file
function stopLoader(loader) {
  clearInterval(loader);
}

// ~~~~~~~~~~~~~~~~~~~~ File management ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

let deleteOldFiles = function() {
  const files = glob.sync("test/visual-regression-test/*.png");

  if (files && typeof files !== "undefined" && files.length > 0) {
    files.forEach(function(file) {
      try {
        fs.unlinkSync(file);
      } catch (error) {
        console.log(error);
      }
    });
  }
};

// ~~~~~~~~~~~~~~~~~~~~ Config start ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if (cmdArg === "config") {
  // load base page and get height then take screenshots of both pages at that size
  timerStart = loader();
  timerCounter = 0;

  // eslint-disable-next-line no-inner-declarations
  function loadYaml(filename) {
    return yaml.safeLoad(fs.readFileSync(filename, "utf8"));
  }

  let vrtConfigData = loadYaml("./test/visual-regression-test/vrt_config.yml");

  imgLocations = vrtConfigData.imgLocations;
  let pagesToTest = vrtConfigData.pagesToTest;
  let screenWidth = vrtConfigData.screenWidth;
  let testEnv = vrtConfigData.testEnv;
  let baseEnv = vrtConfigData.baseEnv;

  for (let pageName in pagesToTest) {
    if (pagesToTest.hasOwnProperty(pageName)) {
      deleteOldFiles();
      getScreenShots(
        pagesToTest[pageName],
        pageName,
        testEnv,
        baseEnv,
        screenWidth
      );
    }
  }
  // quit the driver instance
  driver.quit();
}

// ~~~~~~~~~~~~~~~~~~~~ Single page command line arguments and prompts ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if (cmdArg === "single-page") {
  deleteOldFiles();

  // set options and choices
  const argv = require("yargs")
    .option("page", {})
    .choices("testEnvironment", [])
    .choices("baseEnvironment", [])
    .choices("width", []).argv;

  // get values from the command line
  (async function() {
    // ask which page will be tested
    const pageName =
      argv.pageName ||
      (await prompts({
        type: "text",
        name: "value",
        message: "What page would you like to test?"
      })).value;

    // ask which environment will be tested
    const testEnvironment =
      argv.testEnvironment ||
      (await prompts({
        type: "select",
        name: "value",
        message: "What environment would you like to test?",
        choices: [
          { title: "local", value: "http://localhost:4200" },
          { title: "Production", value: "https://developers.arcgis.com" }
        ]
      })).value;

    // ask which environment is the basis for comparison
    const baseEnvironment =
      argv.baseEnvironment ||
      (await prompts({
        type: "select",
        name: "value",
        message: "What environment would you like to test against?",
        choices: [
          { title: "local", value: "http://localhost:4200" },
          { title: "Production", value: "http://vrt.afd.geocloud.com/" }
        ]
      })).value;

    // ask which page width (in pixels) the browser window will be set to
    const width =
      argv.width ||
      (await prompts({
        type: "select",
        name: "value",
        message: "What browser width would you like to test?",
        choices: [
          { title: "768", value: 768 },
          { title: "1024", value: 1024 },
          { title: "1366", value: 1366 },
          { title: "1440", value: 1440 },
          { title: "1536", value: 1536 },
          { title: "1920", value: 1920 }
        ]
      })).value;

    // after all the arguments are collected and set, call screenshots function with values
    timerStart = loader();
    timerCounter = 0;
    getScreenShots(pageName, pageName, testEnvironment, baseEnvironment, width);
    // quit the driver instance
    driver.quit();
  })();
}

// ~~~~~~~~~~~~~~~~~~~~ Image gathering ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

function getScreenShots(
  pageURL,
  pageName,
  testEnvironment,
  baseEnvironment,
  width,
  height = 1000
) {
  timerCounter++;
  // handle file names that might have "/" in them since the urls used for file paths
  var baseImgName = function(pageName) {
    if (pageName === "/") {
      return imgLocations + "home-base.png";
    } else {
      return (
        imgLocations +
        pageName.replace(/^\/|\/$/g, "").replace(/\//g, "-") +
        "-base.png"
      );
    }
  };

  var testImgName = function(pageName) {
    if (pageName === "/") {
      return imgLocations + "home-test.png";
    } else {
      return (
        imgLocations +
        pageName.replace(/^\/|\/$/g, "").replace(/\//g, "-") +
        "-test.png"
      );
    }
  };

  // set the window size
  windowOptions(width, height);

  // gets the base environment and page
  driver.get(baseEnvironment);

  // gets the base environment and page
  driver.get(baseEnvironment + pageURL);

  driver.sleep(5000);

  // use in-browser javascript to determine the full height (in pixels) of the page
  const windowSize = () => {
    return driver.executeScript("return document.body.parentNode.scrollHeight");
  };

  // re-set the window size using the full page height
  windowOptions(width, windowSize());

  // take a screenshot of the base page and save as png
  driver
    .takeScreenshot()
    .then((image, err) => {
      require("fs").writeFileSync(baseImgName(pageName), image, "base64");

      // get the test page with the same browser instance and take another screenshot
      return driver.get(testEnvironment + pageURL);
    })
    .then(function() {
      driver.sleep(5000);
      return driver.takeScreenshot();
    })
    .then(image => {
      require("fs").writeFileSync(testImgName(pageName), image, "base64");

      // call diff function to look for regressions
      diff(baseImgName(pageName), testImgName(pageName), pageName);
    });
}

// ~~~~~~~~~~~~~~~~~~~~ Image comparison ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

// compare screenshots and look for a diff. If a diff is found call
// genDiffImage function to generate an new diff image
async function diff(baseImgName, testImgName, pageName) {
  looksSame(baseImgName, testImgName, { tolerance: 1 }, function(
    error,
    results
  ) {
    if (error) {
      process.stdout.write(error);
    } else if (!results.equal) {
      genDiffImage(baseImgName, testImgName, pageName);
    } else {
      timerCounter--;
      if (timerCounter === 0) {
        stopLoader(timerStart);
      }
      process.stdout.write(
        "\r" + "No visual difference was found on " + pageName + "\n"
      );
    }
  });
}

// generate an new diff image by comparing screenshots
async function genDiffImage(baseImgName, testImgName, pageName) {
  looksSame.createDiff(
    {
      reference: baseImgName,
      current: testImgName,
      diff: imgLocations + pageName.replace(/\//g, "") + "-diff.png",
      highlightColor: "#ff00ff", // color to highlight the differences
      strict: false, // strict comparsion
      tolerance: 1,
      antialiasingTolerance: 0,
      ignoreAntialiasing: true, // ignore antialising by default
      ignoreCaret: true // ignore caret by default
    },
    function(error) {
      if (error) {
        process.stdout.write(error);
      }
      timerCounter--;
      if (timerCounter === 0) {
        stopLoader(timerStart);
      }
      process.stdout.write(
        "\r" + "UI regression was found on " + pageName + "\n"
      );
    }
  );
}
