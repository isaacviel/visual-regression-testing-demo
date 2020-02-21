# Using the AFD-embedded Visual Regression Tester

The VRT is a tool created by iviel@esri.com for the purpose of comparing differences between two pages to find small changes to the UI that might have occurred unknowingly. Below are some notes on its creation and functionality:

### Terminology
**page:** This is the specific page URI to compare in the two specified environments (base-env vs. test-env.) When specifying this always begin with a `/` e.g. `/java/latest`

**test env:** This is the environment you suspect may have a changed in its appearance and would like to see it compared to a known environment state. `test-env.png` is created from this page.

**base env:**  This is the environment at a known state and forms the basis for comparison. `base-env.png` is created from this page. 

**browser width:** This is the width in pixels that the page will tested at. The choices reflect the most common browser widths used to access the developer site according to Google Analytics. 

**diff.png:** Is the image that will be created if the comparison finds any differences between the `test-env.png` and `base-env.png`. 

### Notes on using the VRT

**Running the VRT from the command line:** Easy! Simply run `npm run vrt` and answer the prompted questions. 

**Running the VRT against a local branch**: In order to compare pages on a locally running branch you must be running that branch with the following npm script `npm run nossl`. This script removes the need to run the site locally with `https://` which causes the chrome webdriver to fail. If you do not plan to compare local branched, there is no need to have the site running at all. 

**No diff.png?** If the VRT does not detect a difference between the pages there will be no `diff.png` generated on that pass. However there might still be an old `diff.png` stored on file. 

### Future: Items to be added in the future 
- Ability to run the VRT again multiple pages via `yaml` file
- Ability to change the tolerance/ change delta of the test via the command line
- Give browser width an option of user input to specify any width
- HTML page output instead of a simple image
- Ability to run on app pages e.g. `/dashboard/` etc
- Add `--help` arg

### Notes:
Libraries used: 
 - https://www.npmjs.com/package/looks-same
 - https://www.npmjs.com/package/selenium-webdriver
 - https://www.npmjs.com/package/prompts
