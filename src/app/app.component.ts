import { Component } from "@angular/core";

@Component({
  selector: "app-root",
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.scss"]
})
export class AppComponent {
  title = "vrt-demo";

  // Set our map properties
  mapCenter = [-116.5403, 33.8258];
  basemapType = "streets-vector";
  mapZoomLevel = 16;

  // See app.component.html
  mapLoadedEvent(status: boolean) {
    console.log("The map loaded: " + status);
  }
}
