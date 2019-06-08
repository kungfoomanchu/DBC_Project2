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
var visdata = [];
console.log(`VisData: ${visdata}`)

// Load data
d3.csv("test_data/BTC.csv", function(error, forceData) {

  // Throw an error if one occurs
  if (error) throw error;

  // Print the forceData
  console.log(forceData);

  // Format the date and cast the force value to a number
  forceData.forEach(function(data) {
    data.date = parseTime(data.date);
    data.price = +data.price;
    visdata.push(data)
  });

  // Configure a time scale
  // d3.extent returns the an array containing the min and max values for the property specified
  var xTimeScale = d3.scaleTime()
    .domain(d3.extent(forceData, data => data.date))
    .range([0, chartWidth]);

  // Configure a linear scale with a range between the chartHeight and 0
  var yLinearScale = d3.scaleLinear()
    .domain([0, d3.max(forceData, data => data.price)])
    .range([chartHeight, 0]);

  // Create two new functions passing the scales in as arguments
  // These will be used to create the chart's axes
  var bottomAxis = d3.axisBottom(xTimeScale);
  var leftAxis = d3.axisLeft(yLinearScale);

  // Configure a line function which will plot the x and y coordinates using our scales
  var drawLine = d3.line()
    .x(data => xTimeScale(data.date))
    .y(data => yLinearScale(data.price));

  // Append an SVG path and plot its points using the line function
  chartGroup.append("path")
    // The drawLine function returns the instructions for creating the line for forceData
    .attr("d", drawLine(forceData))
    .attr("stroke-width", 1)
    .attr("stroke", "red")
    .style("fill", "none")
    .classed("line", true);
const tooltip = svg.append("g");

  // Append an SVG group element to the chartGroup, create the left axis inside of it
  //chartGroup.append("g")
  //  .classed("axis", true)
  //  .call(leftAxis);

  // Append an SVG group element to the chartGroup, create the bottom axis inside of it
  // Translate the bottom axis to the bottom of the page
  //chartGroup.append("g")
  //  .classed("axis", true)
  //  .attr("transform", `translate(0, ${chartHeight})`)
  //  .call(bottomAxis);

  svg.on("touchmove mousemove", function() {
    const {date, price} = bisect(d3.mouse(this)[0]);

    tooltip
         .attr("transform", `translate(${x(date)},${y(price)})`)
        // .call(callout, `${value.toLocaleString(undefined, {style: "currency", currency: "USD"})} ${date.toLocaleString(undefined, {month: "short", day: "numeric", year: "numeric"})}`);
  });

  svg.on("touchend mouseleave", () => tooltip.call(callout, null));

  return svg.node();
});


callout = (g, value) => {
    if (!value) return g.style("display", "none");
  
    g
        .style("display", null)
        .style("pointer-events", "none")
        .style("font", "10px sans-serif");
  
    const path = g.selectAll("path")
      .data([null])
      .join("path")
        .attr("fill", "white")
        .attr("stroke", "black");
  
    const text = g.selectAll("text")
      .data([null])
      .join("text")
      .call(text => text
        .selectAll("tspan")
        .data((value + "").split(/\n/))
        .join("tspan")
          .attr("x", 0)
          .attr("y", (d, i) => `${i * 1.1}em`)
          .style("font-weight", (_, i) => i ? null : "bold")
          .text(d => d));
  
    const {x, y, width: w, height: h} = text.node().getBBox();
  
    text.attr("transform", `translate(${-w / 2},${15 - y})`);
    path.attr("d", `M${-w / 2 - 10},5H-5l5,-5l5,5H${w / 2 + 10}v${h + 20}h-${w + 20}z`);
  }

function bisect() {
    const bisect = d3.bisector(d => d.date).left;
    return mx => {
        const date = x.invert(mx);
        const index = bisect(data, date, 1);
        const a = data[index - 1];
        const b = data[index];
        return date - a.date > b.date - date ? b : a;
    };
}

function y() {
    const y = d3.scaleLinear()
    .domain([0, d3.max(visdata, data => data.price)]).nice()
    .range([svgHeight - margin.bottom, margin.top])
}

function x() { 
    const x = d3.scaleTime()
    .domain(d3.extent(visdata, data => data.date))
    .range([margin.left, svgWidth - margin.right])
}