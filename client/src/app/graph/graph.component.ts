import { Component, OnInit, ViewChild, ElementRef, Input, OnChanges } from '@angular/core';
import { HttpClient } from '@angular/common/http';

declare var Plotly: any;

const sleepLayout = {
  title: 'Amount of Sleep',
  xaxis: {
    title: 'Timestamp',
    showgrid: false,
    zeroline: false
  },
  yaxis: {
    title: 'Number of Hours',
    showline: false
  }
};

const AQILayout = {
  title: 'Air Quality Index',
  xaxis: {
    title: 'Timestamp',
    showgrid: false,
    zeroline: false
  },
  yaxis: {
    title: 'Index Value',
    showline: false
  }
};

const baseURL = 'https://staging.osipi.com/api/v1/Tenants/1f11c599-be17-4812-a72f-00921b7716df/Namespaces/EmergingTech/';
const startIndex = '2019-01-01T00:00:00Z';

@Component({
  selector: 'app-graph',
  templateUrl: './graph.component.html',
  styleUrls: ['./graph.component.css']
})
export class GraphComponent implements OnInit, OnChanges {
  aqiData: any;
  accessToken: any;

  @ViewChild('SleepGraph', { static: true})
  private SleepGraph: ElementRef;

  @ViewChild('AQIGraph', { static: true })
  private AQIGraph: ElementRef;

  sleepData: any;
  // aqiData: any;

  constructor(private httpClient: HttpClient) { }

  ngOnChanges(changes) {
    console.log(changes, this);
  }

  ngOnInit() {
    this.sleepData = [{
      x: [0],
      y: [0],
      name: 'name of graph',
      type: 'scatter'
    }];

    this.aqiData = [{
      x: [0],
      y: [0],
      name: 'name of graph',
      type: 'scatter'
    }];

    this.getToken();
    this.initialPlot();
  }

  getToken() {
    const formData: FormData = new FormData();
    formData.append('grant_type', 'client_credentials');
    formData.append('client_id', 'b156af59-7385-4eca-b980-64c99b5b5b57');
    formData.append('client_secret', 'dT+4abYS06WNXsrxCCeDfOds1vpXunFTAvwtlOp0MZM=');
    this.httpClient.post('https://staging.osipi.com/identity/connect/token', formData).subscribe((data: any) => {
      if (data) {
        this.accessToken = data.access_token;
        this.getAQIStream();
      }
    });
  }

  getAQIStream() {
    const headerDict = {
      Authorization: 'bearer ' + this.accessToken
    };
    this.callOCS_AQI(headerDict);

    setInterval( () => this.callOCS_AQI(headerDict), 30000 / 5);
  }

  callOCS_AQI(headerDict) {
    this.httpClient.get(baseURL + 'Streams/aqistream/Data?startIndex=' + startIndex + '&count=10000',
      {headers: {...headerDict}}).subscribe(data => {
        this.shapeAQIData(data);
    });
  }

  shapeAQIData(data) {
    // Shape data from OCS into x[] and y[].
    const x = [];
    const y = [];
    data.forEach(currentPoint => {
      if (currentPoint.aqi && currentPoint.aqi > -1) {
        x.push(new Date(currentPoint.time));
        y.push(currentPoint.aqi);
      }
    });

    // Re-create AQI Data!
    this.aqiData = [{
      x,
      y,
      name: 'name of graph',
      type: 'scatter'
    }];

    // Shape the update array (with new data).
    const update = {
      x: [[...x]],
      y: [[...y]]
    };

    // Obtain AQI Graph and update!
    const curAQI = document.getElementById('AQIGraph');
    Plotly.restyle(curAQI, update);
  }

  initialPlot() {

    // Graph the initial Sleep Graph!
    this.SleepGraph = Plotly.newPlot(
      this.SleepGraph.nativeElement,
      this.sleepData,
      sleepLayout
    );

    // Graph the initial AQI Info!
    this.AQIGraph = Plotly.newPlot(
      this.AQIGraph.nativeElement,
      this.aqiData,
      AQILayout
    );
  }

}
