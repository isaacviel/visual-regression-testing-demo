import { Component } from "@angular/core";

@Component({
  selector: "app-root",
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.scss"]
})
export class AppComponent {
  title = "vrt-demo";

  // Set our map properties
  mapCenter = [-118.2095, 33.8935];
  basemapType = "dark-gray-vector";
  mapZoomLevel = 9;

  // See app.component.html
  mapLoadedEvent(status: boolean) {
    console.log("The map loaded: " + status);
  }
}
