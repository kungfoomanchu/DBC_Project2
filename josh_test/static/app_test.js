// Define SVG area dimensions
var svgWidth = 2000;
var svgHeight = 1000;

// Define the chart's margins as an object
var margin = {
  top: 60,
  right: 60,
  bottom: 60,
  left: 60
};

// Define dimensions of the chart area
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
var parseTime = d3.timeParse("%m/%d/%Y");

// create empty array to hold data
var visData = [];
console.log(`VisData: ${visData}`)

// array for datapoints on visualization
var itemArray = [
  {
      "item": "bitcoin",
      "name": "Bitcoin",
      "date": "1/9/2014",
      "price": 0
},{
      "item": "bitcoin_max",
      "name": "Bitcoin Peak",
      "date": "12/17/2017",
      "price": 19783.06
},{
      "item": "ps4",
      "name": "PS4",
      "date": "11/15/2016",
      "price": 399
},{
      "item": "pizza",
      "name": "Bitcoin Pizza",
      "date": "05/22/2015",
      "price": 30
},{
      "item": "macbook",
      "name": "MacBook Pro 2012",
      "date": "07/30/2014",
      "price": 1199
},{
      "item": "oculus",
      "name": "Oculus Rift",
      "date": "03/28/2016",
      "price": 599
},{
      "item": "fiftycent",
      "name": "50 Cent",
      "date": "02/11/2014",
      "price": 400000
}]
// print item array
itemArray.forEach(item => console.log(item)); 

// var xScaleLocal = xScale(visData);
// var yScaleLocal = yScale(visData);

// Configure a time scale
// d3.extent returns the an array containing the min and max values for the property specified
function graphIt(graphData){
    
// var xTimeScale = d3.scaleTime()
//     .domain(d3.extent(graphData, data => data.date))
//     .range([0, chartWidth]);
var xScaleLocal = xScale(graphData);

// Configure a linear scale with a range between the chartHeight and 0
// var yLinearScale = d3.scaleLinear()
//     .domain([0, d3.max(graphData, data => data.price)])
//     .range([chartHeight, 0]);
var yScaleLocal = yScale(graphData);

// Configure a line function which will plot the x and y coordinates using our scales
var drawLine = d3.line()
    .x(data => xScaleLocal(data.date))
    .y(data => yScaleLocal(data.price));

// Append an SVG path and plot its points using the line function
chartGroup.append("path")
    // The drawLine function returns the instructions for creating the line for forceData
    .attr("d", drawLine(graphData))
    .attr("stroke-width", 1)
    .attr("stroke", "red")
    .style("fill", "none")
    .classed("line", true);
};

function xScale(graphData){
    var xScale = d3.scaleTime()
        .domain(d3.extent(graphData, data => data.date))
        .range([0, chartWidth]);
    return xScale
};

function yScale(graphData){
    var yScale = d3.scaleLinear()
        .domain([0, d3.max(graphData, data => data.price)])
        .range([chartHeight, 0]);
    return yScale
};

function plotIt(graphData){
    var xScaleLocal = xScale(graphData);
    var yScaleLocal = yScale(graphData);
    var drawLine = d3.line()
        .x(data => xScaleLocal(data.date))
        .y(data => yScaleLocal(data.price));

// Append an SVG path and plot its points using the line function
    chartGroup.append("path")
        // The drawLine function returns the instructions for creating the line for forceData
        .attr("d", drawLine(graphData))
        .attr("stroke-width", 1)
        .attr("stroke", "red")
        .style("fill", "none")
        .classed("line", true);
}

// Load and format data
d3.csv("test_data/BTC.csv", function(error, tempData) {
    // Throw an error if one occurs
    if (error) throw error;
    // print data
    console.log(tempData);
    // Format the date and cast the price value to a number
    tempData.forEach(function(data) {
      data.date = parseTime(data.date);
      data.price = +data.price;
      visData.push(data)
    });
    dateConvert(displayPoints);
    graphIt(visData);
    plotIt(displayData);
});

function dateConvert(tempData) {
    tempData.forEach(function(data){
      data.date = parseTime(data.date)
      displayData.push(data)
    });
}

var displayData = [];

var displayPoints = [
    {
        "date":"4/28/13",
        "price":134.21
    },
    {
        "date":"1/9/2014",
        "price":870.96
    },
    {
        "date":"12/17/2017",
        "price":19140.8
    },
    {
        "date":"11/15/2016",
        "price":711.62
    },
    {
        "date":"5/22/2015",
        "price":240.35
    },
    {
        "date":"7/30/2014",
        "price":567.29
    },
    {
        "date":"3/28/2016",
        "price":424.23
    },
    {
        "date":"2/11/2014",
        "price":672.17
    },
    {
        "date":"11/29/18",
        "price":4278.85
    }
];