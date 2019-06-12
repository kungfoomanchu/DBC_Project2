var svgWidth = 2000;
var svgHeight = 1000;

var margin = {
  top: 60,
  right: 60,
  bottom: 60,
  left: 60
};

var visData = [];
console.log(`VisData: ${visData}`)

var displayData = [];
console.log(`displayData: ${displayData}`)

var chartWidth = svgWidth - margin.left - margin.right;
var chartHeight = svgHeight - margin.top - margin.bottom;

// Select body, append SVG area to it, and set its dimensions
var svg = d3.select("body")
  .append("svg")
  .attr("width", svgWidth)
  .attr("height", svgHeight);

// Append a group area, then set its margins
var chartGroup = svg.append("g")
  .attr("transform", `translate(${margin.left}, ${margin.top})`);

// Configure a parseTime function which will return a new Date object from a string
var parseTime = d3.timeParse("%Y-%m-%d");

function dateConvert(tempData) {
    tempData.forEach(function(data){
        console.log(data)
        let dateString = data.date.split("T");
        data.date = parseTime(dateString[0]);
        data.bitcoin_price = +data.bitcoin_price;
        displayData.push(data)
    });
}

function graphIt(graphData, secondData){
    
    var xScaleLocal = xScale(graphData);

    var yScaleLocal = yScale(graphData);

    var drawLine = d3.line()
        .x(data => xScaleLocal(data.time_period_start))
        .y(data => yScaleLocal(data.price_close));

    chartGroup.append("path")
        .attr("d", drawLine(graphData))
        .attr("stroke-width", 1)
        .attr("stroke", "red")
        .style("fill", "none")
        .classed("line", true);

    chartGroup.selectAll('circle')
        .data(secondData)
        .enter()
        .append("circle")
        .attr("cx", d=>xScaleLocal(d.date))
        .attr("cy", d=>yScaleLocal(d.bitcoin_price))
        .attr("r", '5px')
        .attr("stroke", "black")
        .attr("stroke-width", "1")
        .attr("fill", "red");

    chartGroup.selectAll('image')
        .data(secondData)
        .enter()
        .append("image")
        .attr("x", d=>xScaleLocal(d.date))
        .attr("y", d=>yScaleLocal(d.bitcoin_price))
        .attr('height', 50)
        .attr('width', 50)
        .attr('href', d=>d.svg)
};

function xScale(graphData){
    var xScale = d3.scaleTime()
        .domain(d3.extent(graphData, data => data.time_period_start))
        .range([0, chartWidth]);
    return xScale
}

function yScale(graphData){
    var yScale = d3.scaleLinear()
        .domain([0, d3.max(graphData, data => data.price_close)])
        .range([chartHeight, 0]);
    return yScale
}

d3.json('/static/temp/coin.json', function(tempData) {
    console.log(tempData);
    // Format the date and cast the price value to a number
    tempData.forEach(function(data) {
      data.time_period_start = parseTime(data.time_period_start);
      data.price_close = +data.price_close;
      visData.push(data)
    });
    d3.json('http://127.0.0.1:5000/itemstoo', function(data) {
        console.log(data);
        dateConvert(data);
        graphIt(visData, displayData);
    });
    
})

// Load and format data
// d3.csv("test_data/BTC.csv", function(error, tempData) {
//     // Throw an error if one occurs
//     if (error) throw error;
//     // print data
//     console.log(tempData);
//     // Format the date and cast the price value to a number
//     tempData.forEach(function(data) {
//       data.date = parseTime(data.date);
//       data.price = +data.price;
//       visData.push(data)
//     });
//     dateConvert(displayPoints);
//     graphIt(visData, displayData);
//     // plotIt(displayData);
// });