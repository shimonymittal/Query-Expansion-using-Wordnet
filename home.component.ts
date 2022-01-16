import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpParams } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, tap, map } from 'rxjs/operators';
import { Hits } from "./Hits"
@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  constructor(private http: HttpClient) { }

  query: string = "";
  result: any[] = [];
  queryUrl: string = "http://127.0.0.1:8000/fetch"

  // fetchQueryService(): Observable<Hits[]>{
  //   return this.http.get<Hits[]>(this.queryUrl).pipe(
  //     tap(data => console.log('All: ' + JSON.stringify(data))),
  //     catchError(this.handleError)
  //   );
  // }

  fetchQuery(query: string){
    //this.result = query;
    let params = new HttpParams().set("q",query);
    this.http.get<Hits>(this.queryUrl, {params: params}).subscribe(data => {
        this.result = data.hits.hits;
        console.log(this.result);
    })
  }

  ngOnInit(): void {
  }

  private handleError(err: HttpErrorResponse) {
    // in a real world app, we may send the server to some remote logging infrastructure
    // instead of just logging it to the console
    let errorMessage = '';
    if (err.error instanceof ErrorEvent) {
      // A client-side or network error occurred. Handle it accordingly.
      errorMessage = `An error occurred: ${err.error.message}`;
    } else {
      // The backend returned an unsuccessful response code.
      // The response body may contain clues as to what went wrong,
      errorMessage = `Server returned code: ${err.status}, error message is: ${err.message}`;
    }
    console.error(errorMessage);
    return throwError(errorMessage);
  }

}
