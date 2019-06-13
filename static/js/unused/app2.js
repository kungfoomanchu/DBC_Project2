// from data.js
//var tableData = data;

//console.log(tableData);

// YOUR CODE HERE!
var submit = d3.select("#filter-btn");
var tbody = d3.select("tbody");
var output = d3.select(".table table-striped");

var canvas_Xsize = 510
var canvas_Ysize = 510

var quantity;
var data = new Array();
var xpos = 1; //starting xpos and ypos at 1 so the stroke will show when we make the grid below
var ypos = 1;

var rowCount = Math.ceil(Math.sqrt(quantity));
var colCount = Math.ceil(Math.sqrt(quantity));

var width = canvas_Xsize/rowCount;
var height = canvas_Ysize/colCount;


function gridData() {
  
var gridCount = 0;

let flatData = [];
for(let q =0; q<quantity;q++){
  let rowid = Math.floor(q/rowCount)
  let colid = q%rowCount
  let d = {
    x: rowid,
    y: colid,
    width: width,
    height: height
  }
  flatData.push(d);
}
console.log(flatData);
  // iterate for rows 
  for (var row = 0; row < rowCount; row++) {
      data.push( new Array() );
      
      // iterate for cells/columns inside rows
      for (var column = 0; column < colCount; column++) {
          data[row].push({
              x: xpos,
              y: ypos,
              width: width,
              height: height
          })
          // increment the x position. I.e. move it over by (width variable)
          gridCount++;
          if (gridCount < quantity) {
          xpos += width;
          }
          
      }
      // reset the x position after a row is complete
      
      xpos = 1;
      // increment the y position for the next row. Move it down by (height variable)
      ypos += height; 
  }
  return flatData;

}

var gridData = gridData();    
// I like to log the data to the console for quick debugging
console.log(gridData);

var grid = d3.select("#grid")
    .append("svg")
    .attr("width", canvas_Xsize + "px")
    .attr("height",canvas_Ysize + "px");


var squares = grid.selectAll('.square')
.data(gridData)
    .enter().append("image")
    .attr("x", function(d) { return d.width * d.x })
    .attr("y", function(d) { return d.height * d.y })
    .attr('height', height)
    .attr('width', width )
    //.attr("text-anchor","middle")
    //.attr("dy",".35em")
    .attr('href',function(d) { return 'static/images/bitcoin.svg'})
// var row = grid.selectAll(".row")
//     .data(gridData)
//     .enter().append("g")
//     .attr("class", "row");

// // var column = row.selectAll(".square")
// //     .data(function(d) { return d; })
// //     .enter().append("rect")
// //     .attr("class","square")
// //     .attr("x", function(d) { return d.x; })
// //     .attr("y", function(d) { return d.y; })
// //     .attr("width", function(d) { return d.width; })
// //     .attr("height", function(d) { return d.height; })
// //     .style("fill", "#fff")
// //     .style("stroke", "#222")
    
    

// var column = row.selectAll(".square")
//   .data(function(d) {return d;})
//   .enter().append("image")
//     .attr("x", function(d) { return d.x })
//     .attr("y", function(d) { return d.y })
//     .attr('height', height)
//     .attr('width', width )
//     //.attr("text-anchor","middle")
//     //.attr("dy",".35em")
//     .attr('href',function(d) { return 'static/images/bitcoin.svg'});

