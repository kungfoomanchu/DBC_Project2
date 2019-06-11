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
var parseTime = d3.timeParse("%m/%d/%y");

function dateConvert(tempData) {
    tempData.forEach(function(data){
      data.date = parseTime(data.date)
      displayData.push(data)
    });
}

function graphIt(graphData, secondData){
    
    var xScaleLocal = xScale(graphData);

    var yScaleLocal = yScale(graphData);

    var drawLine = d3.line()
        .x(data => xScaleLocal(data.date))
        .y(data => yScaleLocal(data.price));

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
        .attr("cy", d=>yScaleLocal(d.price))
        .attr("r", '10px')
        .attr("stroke", "black")
        .attr("stroke-width", "5")
        .attr("fill", "black");
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
    graphIt(visData, displayData);
    // plotIt(displayData);
});

var displayPoints = [
    {
        "date":"4/28/13",
        "price":134.21
    },
    {
        "date":"1/9/14",
        "price":870.96
    },
    {
        "date":"12/17/17",
        "price":19140.8
    },
    {
        "date":"11/15/16",
        "price":711.62
    },
    {
        "date":"5/22/15",
        "price":240.35
    },
    {
        "date":"7/30/14",
        "price":567.29
    },
    {
        "date":"3/28/16",
        "price":424.23
    },
    {
        "date":"2/11/14",
        "price":672.17
    },
    {
        "date":"11/29/18",
        "price":4278.85
    }
];