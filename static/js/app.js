// YOUR CODE HERE!
var submit = d3.select("#filter-btn");
var tbody = d3.select("tbody");
var output = d3.select(".table table-striped");

var canvas_Xsize = 800
var canvas_Ysize = 800



submit.on("click", function () {

  var quantity;
  var data = new Array();
  var xpos = 1; //starting xpos and ypos at 1 so the stroke will show when we make the grid below
  var ypos = 1;


  // Prevent the page from refreshing
  d3.event.preventDefault();
  d3.select("svg").remove();
  d3.select("svg").remove();
  //Get TBody
  //var tableEmpty = document.getElementById('ufo-table');
  //console.log(tableEmpty)

  // Get the value property of the input element
  var dropdown = document.getElementById('myList');
  var strUser = dropdown.options[dropdown.selectedIndex].value;
  console.log(strUser)

  var inputElement = d3.select("#myList");
  var inputValue = inputElement.property("value");
  item = inputValue;
  console.log(item);


  //////////////////////
  // Start JSON Quantity Interpretation
  //////////////////////

  /* global Plotly */

  var url =
    `http://127.0.0.1:5000/quantity_json/${item}`;

  // function unpack(rows, index) {
  //   return rows.map(function(row) {
  //     return row[index];
  //   });
  // }

  function getQuantity(cb) {

    d3.json(url).then(function (data) {
      // To see what the data looks like, check the console
      console.log(data[0]);
      // Grab values from the data json object to build the plots
      var item_name = data[0].item_name;
      var item_quantity_current = data[0].item_quantity_max;
      var item_quantity_max = data[0].item_quantity_current;
      var item_svg = data[0].item_svg;

      var item_quantities = [item_name, item_quantity_current, item_quantity_max, item_svg]
      console.log(item_quantities)
      //Plotly.newPlot("plot", data, layout);

      cb(item_quantities);
    });
  }


  // function getItems() {
  //   d3.json('http://127.0.0.1:5000/items').then(function(data) {

  //     // To see what the data looks like, check the console
  //     console.log(data.length);

  //     // Grab values from the data json object to build the plots
  //     for( i = 0; i <= data.length; i++){
  //     var item_date = data[i].date;
  //     var item_item = data[i].item;
  //     var item_name = data[i].name;
  //     var item_price = data[i].price;
  //     console.log(`${item_date}, ${item_item}, ${item_name}, ${item_price}`);
  //     }
  //     //console.log(`${item_date}, ${item_item}, ${item_name}, ${item_price}`)
  //     //Plotly.newPlot("plot", data, layout);

  //   });
  // }

  getQuantity(function (data_of_item) {
    //getItems();
    console.log(data_of_item);


    var rowCount = Math.ceil(Math.sqrt(data_of_item[1]));
    var colCount = Math.ceil(Math.sqrt(data_of_item[1]));
    console.log(rowCount);
    var width = canvas_Xsize / rowCount;
    var height = canvas_Ysize / colCount;
    console.log(width);


    function gridData() {
      var gridCount = 0;

      let flatData = [];
      for (let q = 0; q < data_of_item[1]; q++) {
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
          if (gridCount < data_of_item[1]) {
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
        return data_of_item[3]
      })



    function gridData2() {
      var gridCount = 0;

      let flatData = [];
      for (let q = 0; q < data_of_item[2]; q++) {
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
          if (gridCount < data_of_item[2]) {
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

    var gridData2 = gridData2();
    // I like to log the data to the console for quick debugging
    console.log(gridData2);

    var grid2 = d3.select("#grid2")
      .append("svg")
      .attr("width", canvas_Xsize + "px")
      .attr("height", canvas_Ysize + "px");

    var squares = grid2.selectAll('.square')
      .data(gridData2)
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
        return data_of_item[3]
      })


    var max_display = Math.ceil(data_of_item[1]);
    document.getElementById("insert").innerHTML = max_display;
    var current_display = Math.ceil(data_of_item[2]);
    document.getElementById("insert2").innerHTML = current_display;

  });




})