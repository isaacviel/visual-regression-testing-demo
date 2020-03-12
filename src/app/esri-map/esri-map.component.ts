/*
  Copyright 2019 Esri
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
*/

import {
  Component,
  OnInit,
  OnDestroy,
  ViewChild,
  ElementRef,
  Input,
  Output,
  EventEmitter
} from "@angular/core";
import esri = __esri; // Esri TypeScript Types
import esriConfig from "esri/config";
import Map from "esri/Map";
import MapView from "esri/views/MapView";
import FeatureLayer from "esri/layers/FeatureLayer";

@Component({
  selector: "app-esri-map",
  templateUrl: "./esri-map.component.html",
  styleUrls: ["./esri-map.component.scss"]
})
export class EsriMapComponent implements OnInit, OnDestroy {
  @Output() mapLoadedEvent = new EventEmitter<boolean>();

  // The <div> where we will place the map
  @ViewChild("mapViewNode", { static: true }) private mapViewEl: ElementRef;

  private _zoom = 10;
  private _center: Array<number> = [-12972840.433435235, 4005469.147696632];
  private _basemap = "streets-night-vector";
  private _loaded = false;
  private _view: esri.MapView = null;

  get mapLoaded(): boolean {
    return this._loaded;
  }

  @Input()
  set zoom(zoom: number) {
    this._zoom = zoom;
  }

  get zoom(): number {
    return this._zoom;
  }

  @Input()
  set center(center: Array<number>) {
    this._center = center;
  }

  get center(): Array<number> {
    return this._center;
  }

  @Input()
  set basemap(basemap: string) {
    this._basemap = basemap;
  }

  get basemap(): string {
    return this._basemap;
  }

  constructor() {}

  async initializeMap() {
    const DEFAULT_WORKER_URL = "https://js.arcgis.com/4.14/";
    const DEFAULT_LOADER_URL = `${DEFAULT_WORKER_URL}dojo/dojo-lite.js`;

    esriConfig.workers.loaderUrl = DEFAULT_LOADER_URL;
    esriConfig.workers.loaderConfig = {
      baseUrl: `${DEFAULT_WORKER_URL}dojo`,
      packages: [
        { name: "esri", location: `${DEFAULT_WORKER_URL}esri` },
        { name: "dojo", location: `${DEFAULT_WORKER_URL}dojo` },
        { name: "dojox", location: `${DEFAULT_WORKER_URL}dojox` },
        { name: "dstore", location: `${DEFAULT_WORKER_URL}dstore` },
        { name: "moment", location: `${DEFAULT_WORKER_URL}moment` },
        { name: "@dojo", location: `${DEFAULT_WORKER_URL}@dojo` },
        {
          name: "cldrjs",
          location: `${DEFAULT_WORKER_URL}cldrjs`,
          main: "dist/cldr"
        },
        {
          name: "globalize",
          location: `${DEFAULT_WORKER_URL}globalize`,
          main: "dist/globalize"
        },
        {
          name: "maquette",
          location: `${DEFAULT_WORKER_URL}maquette`,
          main: "dist/maquette.umd"
        },
        {
          name: "maquette-css-transitions",
          location: `${DEFAULT_WORKER_URL}maquette-css-transitions`,
          main: "dist/maquette-css-transitions.umd"
        },
        {
          name: "maquette-jsx",
          location: `${DEFAULT_WORKER_URL}maquette-jsx`,
          main: "dist/maquette-jsx.umd"
        },
        { name: "tslib", location: `${DEFAULT_WORKER_URL}tslib`, main: "tslib" }
      ]
    };

    // Configure the Map
    const mapProperties: esri.MapProperties = {
      basemap: this._basemap
    };

    const map = new Map(mapProperties);

    const tosMarker = {
      type: "simple",
      symbol: {
        type: "picture-marker",
        url: "/assets/img/tos.png",
        width: "32px",
        height: "32px"
      }
    };

    const locationsLayer = new FeatureLayer({
      url:
        "https://services9.arcgis.com/5JLHCUOlymM54r78/arcgis/rest/services/star_trek_locations/FeatureServer/0",
      renderer: tosMarker
    });
    map.layers.add(locationsLayer);

    // Initialize the MapView
    const mapViewProperties: esri.MapViewProperties = {
      container: this.mapViewEl.nativeElement,
      center: this._center,
      zoom: this._zoom,
      map: map
    };

    this._view = new MapView(mapViewProperties);
    // wait for the map to load
    await this._view.when();
    return this._view;
  }

  ngOnInit() {
    // Initialize MapView and return an instance of MapView
    this.initializeMap().then(mapView => {
      // The map has been initialized
      console.log("mapView ready: ", mapView.ready);
      this._loaded = mapView.ready;
      this.mapLoadedEvent.emit(true);
    });
  }

  ngOnDestroy() {
    if (this._view) {
      this._view.container = null;
    }
  }
}
