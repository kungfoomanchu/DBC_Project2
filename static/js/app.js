// from data.js
var tableData = data;

console.log(tableData);

// YOUR CODE HERE!
var submit = d3.select("#filter-btn");
var tbody = d3.select("tbody");
var output = d3.select(".table table-striped");

var canvas_Xsize = 510
var canvas_Ysize = 510


submit.on("click", function () {

  var quantity;
  var data = new Array();
  var xpos = 1; //starting xpos and ypos at 1 so the stroke will show when we make the grid below
  var ypos = 1;


  // Prevent the page from refreshing
  d3.event.preventDefault();

  //Get TBody
  //var tableEmpty = document.getElementById('ufo-table');
  //console.log(tableEmpty)

  // Get the value property of the input element
  var dropdown = document.getElementById('myList');
  var strUser = dropdown.options[dropdown.selectedIndex].value;
  console.log(strUser)

  var inputElement = d3.select("#datetime");
  var inputValue = inputElement.property("value");
  quantity = parseInt(inputValue);
  //var inputValue = strUser
  console.log(quantity);

  var rowCount = Math.ceil(Math.sqrt(quantity));
  var colCount = Math.ceil(Math.sqrt(quantity));
  console.log(rowCount);
  var width = canvas_Xsize / rowCount;
  var height = canvas_Ysize / colCount;
  console.log(width);

  // if (strUser === 'datetime'){
  //   var filteredData = tableData.filter(tableData => tableData.datetime === inputValue);
  // } else if (strUser === 'city') {
  //   var filteredData = tableData.filter(tableData => tableData.city === inputValue);
  // } else if (strUser === 'state') {
  //   var filteredData = tableData.filter(tableData => tableData.state === inputValue);
  // } else if (strUser === 'country') {
  //   var filteredData = tableData.filter(tableData => tableData.country === inputValue);
  // } else if (strUser === 'shape') {
  //   var filteredData = tableData.filter(tableData => tableData.shape === inputValue);
  // }
  // console.log(filteredData);



  function gridData() {
    var gridCount = 0;

    let flatData = [];
    for (let q = 0; q < quantity; q++) {
      let rowid = Math.floor(q / rowCount)
      let colid = q % rowCount
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
      data.push(new Array());

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
    .attr("height", canvas_Ysize + "px");

  var squares = grid.selectAll('.square')
    .data(gridData)
    .enter().append("image")
    .attr("x", function (d) {
      return d.width * d.x
    })
    .attr("y", function (d) {
      return d.height * d.y
    })
    .attr('height', height)
    .attr('width', width)
    //.attr("text-anchor","middle")
    //.attr("dy",".35em")
    .attr('href', function (d) {
      return 'static/images/bitcoin.svg'
    })
  // var row = grid.selectAll(".row")
  //     .data(gridData)
  //     .enter().append("g")
  //     .attr("class", "row");

});


//////////////////////
// Start JSON Quantity Interpretation
//////////////////////
// This variable will have to become dynamic
item = "ps4"
/* global Plotly */
var url =
  `http://localhost:5000/quantity_json/${item}`;

function unpack(rows, index) {
  return rows.map(function(row) {
    return row[index];
  });
}

function getQuantity() {
  d3.json(url).then(function(data) {

    // To see what the data looks like, check the console
    console.log(data)

    // Grab values from the data json object to build the plots
    var item_name = data.item_name;
    var item_quantity_current = data.item_quantity_max;
    var item_quantity_max = data.item_quantity_current;
    var item_svg = data.svg;

    console.log(`${item_name}, ${item_quantity_current}, ${item_quantity_max}, ${item_svg}`)
    //Plotly.newPlot("plot", data, layout);

  });
}

getQuantity();
//////////////////////
// End JSON Quantity Interpretation
//////////////////////