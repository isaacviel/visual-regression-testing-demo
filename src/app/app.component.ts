import { Component } from "@angular/core";

@Component({
  selector: "app-root",
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.scss"]
})
export class AppComponent {
  title = "vrt-demo";

  // Set our map properties
  mapCenter = [-118.3862, 34.1423];
  basemapType = "gray-vector";
  mapZoomLevel = 9;

  // See app.component.html
  mapLoadedEvent(status: boolean) {
    console.log("The map loaded: " + status);
  }
}
