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

// Define the div for the tooltip
var div = d3.select("body").append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

var bigdiv = d3.select("body").append("div")
    .attr("class", "display")
    .style("opacity", 0);

var bigdivon = false;

// Select body, append SVG area to it, and set its dimensions
var svg = d3.select("body")
    .append("svg")
    .attr("width", svgWidth)
    // .attr("width", "100%")
    .attr("height", svgHeight);

// create filter for drop shadow effect
var defs = svg.append("defs");
var filter = defs.append("filter")
    .attr("id", "drop-shadow")
    .attr("height", "130%");

filter.append("feGaussianBlur")
    .attr("in", "SourceAlpha")
    .attr("stdDeviation", 0)
    .attr("result", "blur");

filter.append("feOffset")
    .attr("in", "blur")
    .attr("dx", 0)
    .attr("dy", 0)
    .attr("result", "offsetBlur");

var feMerge = filter.append("feMerge");
feMerge.append("feMergeNode")
    .attr("in", "offsetBlur")
feMerge.append("feMergeNode")
    .attr("in", "SourceGraphic");

// svg.addEventListener('click', (e) => {
//     if (!(e.target === bigdiv) && !bigdiv.contains(e.target)) {
//         console.log('Click outside');
//     } else {
//         console.log('Click inside');
//     }
//     });

// Append a group area, then set its margins
var chartGroup = svg.append("g")
    .attr("transform", `translate(${margin.left}, ${margin.top})`);

// Configure a parseTime function which will return a new Date object from a string
var parseTime = d3.timeParse("%Y-%m-%d");
var formatTime = d3.timeFormat("%m/%d/%y");

function dateConvert(tempData) {
    tempData.forEach(function (data) {
        console.log(data)
        let dateString = data.date.split("T");
        data.date = parseTime(dateString[0]);
        data.bitcoin_price = +data.bitcoin_price;
        displayData.push(data)
    });
}

function graphIt(firstData, secondData) {

    var xScaleLocal = xScale(firstData);

    var yScaleLocal = yScale(firstData);

    var drawLine = d3.line()
        .x(data => xScaleLocal(data.time_period_start))
        .y(data => yScaleLocal(data.price_close));

    chartGroup.append("path")
        .attr("d", drawLine(firstData))
        .attr("stroke-width", 2)
        .attr("stroke", "#00ffcc")
        .style("fill", "none")
        .classed("line", true)
        .style("filter", "url(#drop-shadow)")
        .transition()
        .duration(2000)
        .attr("stroke", "white");

    chartGroup.selectAll('circle')
        .data(secondData)
        .enter()
        .append("circle")
        .attr("cx", d => xScaleLocal(d.date))
        .attr("cy", d => yScaleLocal(d.bitcoin_price))
        .attr("r", '7px')
        .attr("stroke", "white")
        .attr("stroke-width", "2")
        .attr("fill", "red")
        .style("opacity", 0)
        .transition()
        .duration(3000)
        .style("opacity", 1);

    chartGroup.selectAll('rect')
        .data(secondData)
        .enter()
        .append("rect")
        .attr("x", d => xScaleLocal(d.date))
        .attr("y", d => yScaleLocal(d.bitcoin_price))
        .attr('height', 50)
        .attr('width', 50)
        .attr("stroke", "white")
        .attr("stroke-width", "2")
        .attr("fill", "#d3d3d3")
        .attr("id", secondData.item)
        .style("opacity", 0)
        .transition()
        .duration(3000)
        .style("opacity", 1);

    chartGroup.selectAll('image')
        .data(secondData)
        .enter()
        .append("image")
        .attr("x", d => xScaleLocal(d.date))
        .attr("y", d => yScaleLocal(d.bitcoin_price))
        .attr('height', 50)
        .attr('width', 50)
        .attr('href', d => d.svg)
        .style("opacity", 0)
        .on("mouseover", function (d, i) {
            console.log("Mouseover:", d, i);
            d3.select(this)
                .transition()
                .duration(200)
                .style("opacity", .5);
            div.transition()
                .duration(200)
                .style("opacity", .9);
            div.html(d.name + "<br/>" + formatTime(d.date) + "<br/>" + `$${d.bitcoin_price}`)
                .style("left", (d3.select(this).attr("x") + 100) + "px")
                .style("top", (d3.select(this).attr("y") + 100) + "px");
        })
        .on("mouseout", function (d, i) {
            d3.select(this)
                .transition()
                .duration(500)
                .style("opacity", 1);
            div.transition()
                .duration(500)
                .style("opacity", 0);
        })
        .on("click", function (d, i) {
            console.log("Click:", d, i);
            bigdiv.transition()
                .duration(500)
                .style("opacity", .9);
            bigdiv.html(d.name + "<br/>" + formatTime(d.date) + "<br/>" + `$${d.bitcoin_price}`)
                .style("left", "100px")
                .style("top", "100px");
            bigdivon = true;
        })
        .transition()
        .duration(3000)
        .style("opacity", 1)
};

function shadow() {
    filter.select('feGaussianBlur')
        .transition()
        .duration(4000)
        .attr("stdDeviation", 1.5);
    filter.select('feOffset')
        .transition()
        .duration(4000)
        .attr("dx", 2)
        .attr("dy", 2);
}

function xScale(graphData) {
    var xScale = d3.scaleTime()
        .domain(d3.extent(graphData, data => data.time_period_start))
        .range([0, chartWidth]);
    return xScale
}

function yScale(graphData) {
    var yScale = d3.scaleLinear()
        .domain([0, d3.max(graphData, data => data.price_close)])
        .range([chartHeight, 0]);
    return yScale
}

d3.json('/static/temp/coin.json', function (tempData) {
    console.log(tempData);
    // Format the date and cast the price value to a number
    tempData.forEach(function (data) {
        data.time_period_start = parseTime(data.time_period_start);
        data.price_close = +data.price_close;
        visData.push(data)
    });
    d3.json('http://127.0.0.1:5000/itemstoo', function (data) {
        console.log(data);
        dateConvert(data);
        graphIt(visData, displayData);
        shadow();
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