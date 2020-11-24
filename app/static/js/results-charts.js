function render_charts(zipped_pos_total, zipped_pos_inc, user_state_specifics){

  Chart.defaults.global.animation.duration = 3000;
  //<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.min.js" integrity="sha512-d9xgZrVZpmmQlfonhQUvTR7lMPtO7NkZMkA0ABN3PHCbKA5nqylQ/yWlFAyY6hYgdF1Qh6nYiuADWwKB4C2WSw==" crossorigin="anonymous"></script>
  //<script src="https://unpkg.com/chartjs-gauge@0.2.0/dist/chartjs-gauge.js"></script>
  //<!-- Import D3 Scale Chromatic via CDN -->
  //<script src="https://d3js.org/d3-color.v1.min.js"></script>
  //<script src="https://d3js.org/d3-interpolate.v1.min.js"></script>
  //<script src="https://d3js.org/d3-scale-chromatic.v1.min.js"></script>

  // --------------- GAUGE CHART ---------------
  // get chart canvas
  var ctx = document.getElementById("gaugeChart").getContext("2d");
  // get chart data
  var score = 0
  score += document.getElementById("score").innerHTML
  // create chart using the canvas
  var chart = new Chart(ctx, {
    type: 'gauge',
    data: {
      datasets: [{
        value: score,
        data: [25, 50, 75, 100],
        backgroundColor: ['rgba(88, 214, 141, 1)', 'rgba(255, 195, 0, 1)', 'rgba(255, 87, 51, 1)', 'rgba(199, 0, 57, 1)'],
      }]
    },
    options: {
      needle: {
        radiusPercentage: 4,
        widthPercentage: 5,
        lengthPercentage: 80,
        color: 'rgba(0, 0, 0, 1)'
      },
      valueLabel: {
        display: false,
      },
      responsive: false,
      events: ['click'], // prevents a weird hover bug
    }
  });


  // Global parameters: do not resize the chart canvas

  var low_risk_events = user_state_specifics["low_risk_events"];
  var mod_risk_events = user_state_specifics["mod_risk_events"];
  var mod_high_risk_events = user_state_specifics["mod_high_risk_events"];
  var high_risk_events = user_state_specifics["high_risk_events"];
  var total_events = 0

  total_events += (low_risk_events*2) + (mod_risk_events*4) + (mod_high_risk_events*8) + (high_risk_events*16)
    
  // --------------- PIE CHART 1 ---------------
  // get chart canvas
  try{
    var ctx = document.getElementById("pieChart1").getContext("2d");
    // create chart using the canvas
    var chart = new Chart(ctx, {
      type: 'pie',
      data: {
        datasets: [{
          // displays each event type by percentage of total risk score to 2 decimals
          data: [(Math.round(low_risk_events*2/total_events*(100))/100), (Math.round(mod_risk_events*4/total_events*(100))/100), (Math.round(mod_high_risk_events*8/total_events*(100))/100), 
          (Math.round(high_risk_events*16/total_events*(100))/100)],
          backgroundColor: ['rgba(88, 214, 141, 1)', 'rgba(255, 195, 0, 1)', 'rgba(255, 87, 51, 1)', 'rgba(199, 0, 57, 1)'],
        }],
        labels: [
          'Low risk',
          'Moderate risk',
          'Moderate-High risk',
          'High risk'
        ]
      },
      options: {
        cutoutPercentage: 50,
        legend: {
          display: true,
          position: 'top',
          align: 'start',
          labels: {
            boxWidth: 20,
            fontSize: 14,
            fontStyle: 'bold',
          },
        },
        events: ['click'], // prevents a weird hover bug
      },
    });
  }
  catch(err){
    console.log('No activities selected')
  }

  // --------------- PIE CHART 2 ---------------
  // get chart canvas
  try{
    var ctx = document.getElementById("pieChart2").getContext("2d");
    var hospitalized = user_state_specifics["hosp_currently"];
    console.log(hospitalized);
    var icu = user_state_specifics["icu_currently"];
    var nonICU = hospitalized - icu;
    // create chart using the canvas
    var pieChart2 = new Chart(ctx, {
      type: 'pie',
      data: {
        datasets: [{
          // displays each event type by percentage of total risk score to 2 decimals
          data: [ nonICU , icu ],
          backgroundColor: ['rgba(255, 87, 51, 1)', 'rgba(199, 0, 57, 1)'],
        }],
        labels: ['In hospital (general)', 'In hospital ICUs'],
      },
      options: {
        cutoutPercentage: 0,
        legend: {
          display: true,
          position: 'top',
          align: 'start',
          labels: {
            boxWidth: 20,
            fontSize: 14,
            fontStyle: 'bold',
          },
        },
        responsive: false,
        events: ['click'], // prevents a weird hover bug
      },
    });
  } 
  catch(err) {
    console.log("no hospitalization data");
  }

  // --------------- Bar CHART  --------------
  // need to copy data sent by routes.py into javascript variables
  // Source: https://medium.com/code-nebula/automatically-generate-chart-colors-with-chart-js-d3s-color-scales-f62e282b2b41
  function createBarChart(chartId, chartData, colorScale, colorRangeInfo) {
  // Grab chart element by id 
  const chartElement = document.getElementById(chartId);
  const dataLength = chartData.data.length;
  // Create color array 
  var COLORS = interpolateColors(dataLength, colorScale, colorRangeInfo);
  // Create chart 
  const myChart = new Chart(chartElement, {
  type: 'bar',
  data: {
    labels: chartData.labels,
    datasets: [
      {
        backgroundColor: COLORS,
        hoverBackgroundColor: COLORS,
        data: chartData.data
      }
    ],
  },
  options: {
    scales: {
      xAxes: [
        {
          ticks: {
              fontSize: 11,
          },
      }],
      yAxes: [{
          ticks: {
              fontSize: 14,
          },
      }],
  },
    responsive: true,
    legend: {
      display: false,
    },
    hover: {
      onHover: function(e) {
        var point = this.getElementAtEvent(e);
        e.target.style.cursor = point.length ? 'pointer' : 'default';
      },
    },
  },
    events: ['click'], // prevents a weird hover bug
  });
    return myChart;
  }
  // fetch total and daily positive cases from routing page
  //var pos = JSON.parse('{{zipped_pos_total | tojson}}');
  //var pos_inc = JSON.parse('{{zipped_pos_inc | tojson}}');
  var pos = zipped_pos_total;
  var pos_inc = zipped_pos_inc;
  // sort the states by total positive cases in descending order
  var pos_sorted = sortJsObject(pos);
  // sort the states by daily positive cases in descending order
  var pos_inc_sorted = sortJsObject(pos_inc);
  // for debugging
  console.log('pos: ' + pos);
  console.log('pos_inc: ' + pos_inc);
  console.log('pos_sorted: ' + pos_sorted);
  // Sort total cases in Descending order and then find the corresponding state code
  function get_bar_chart_data(dict, dict_sorted){
    var i;
    var data = [];
    var labels = [];
    var label_key = [];
    var label_dict = {'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas', 'AS': 'American Samoa', 'AZ': 'Arizona', 'CA': 'California', 'CO': 'Colorado', 
              'CT': 'Connecticut', 'DC': 'Washington DC', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'GU': 'Guam', 'HI': 'Hawaii', 'IA': 'Iowa', 'ID': 'Idaho', 
              'IL': 'Illinois', 'IN': 'Indiana', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisianna', 'MA': 'Massachusettes', 'MD': 'Maryland', 'ME': 'Maine', 
              'MI': 'Michigan', 'MN': 'Minnisota', 'MO': 'Missouri', 'MP': 'Nortern Mariana Islands', 'MS': 'Mississippi', 
              'MT': 'Montana', 'NC': 'North Carolina', 'ND': 'North Dakota', 'NE': 'Nebraska', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NV': 'Nevada',  
              'NY': 'New York', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'PR': 'Puerto Rico',
              'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VA': 'Virginia', 
              'VI': 'Virgin Islands', 'VT': 'Vermont', 'WA': 'Washington', 'WI': 'Wisconsin', 'WV': 'West Virginia', 'WY': 'Wyoming'};
    console.log("in function");
    for (i = 55; i > 45; i--) {
    for (const key in dict) {
      if(dict.hasOwnProperty(key)){
          if(dict[key] == dict_sorted[i]){
            // add data and label for displaying in chart
            data.push(dict[key]);
            // label is just the 2 letter state code
            label_key.push(key);
        }
      }
    }
    }
    // need to get full state name by matching to state code
    for (i = 0; i < 10; i++) {
    for (const key in label_dict) {
      if(label_dict.hasOwnProperty(key)){
          if(key == label_key[i]){
            labels.push(label_dict[key]);
          }
      }
    }
    }
    console.log("data in func: " + data);
    console.log("labels in func: " + labels);
    return {
      data, 
      labels
        }
    }
    var {data, labels} = get_bar_chart_data(pos, pos_sorted);
    var data_total = data;
    var labels_total = labels;
    var {data, labels} = get_bar_chart_data(pos_inc, pos_inc_sorted);
    var data_daily = data;
    var labels_daily = labels;
    console.log("data out func: " + data_total);
    console.log("labels out func: " + labels_total);
    console.log("data out func: " + data_daily);
    console.log("labels out func: " + labels_daily);
    const chartData_total = {
    labels: labels_total,
    data: data_total,
    };
    const chartData_daily = {
    labels: labels_daily,
    data: data_daily,
    };
    const colorScale = d3.interpolateInferno;
    const colorRangeInfo = {
    colorStart: 0,
    colorEnd: 1,
    useEndAsStart: false,
  }; 
  //var colorScale = chart_color();
  function calculatePoint(i, intervalSize, colorRangeInfo) {
    var { colorStart, colorEnd, useEndAsStart } = colorRangeInfo;
    return (useEndAsStart
    ? (colorEnd - (i * intervalSize))
    : (colorStart + (i * intervalSize)));
  }
  // Must use an interpolated color scale, which has a range of [0, 1] 
  function interpolateColors(dataLength, colorScale, colorRangeInfo) {
    var { colorStart, colorEnd } = colorRangeInfo;
    var colorRange = colorEnd - colorStart;
    var intervalSize = colorRange / dataLength;
    var i, colorPoint;
    var colorArray = [];
    for (i = 0; i < dataLength; i++) {
      colorPoint = calculatePoint(i, intervalSize, colorRangeInfo);
      colorArray.push(colorScale(colorPoint));
    }
    return colorArray;
  }  
  createBarChart('total-pos-chart', chartData_total, colorScale, colorRangeInfo);
  createBarChart('daily-pos-chart', chartData_daily, colorScale, colorRangeInfo);
  //  Sorts dictionary by Value from smallest to largest
  // https://stackoverflow.com/questions/25500316/sort-a-dictionary-by-value-in-javascript
  function sortJsObject(dict) {
    var keys = [];
    for(var key in dict) { 
      keys[keys.length] = key;
    }
    var values = []; 
    for(var i = 0; i < keys.length; i++) {
        values[values.length] = dict[keys [i]];
    }
    var sortedValues = values.sort(sortNumber);
    return sortedValues;     
  }
    function sortNumber(a,b) {
      return a - b;
    }
  }






