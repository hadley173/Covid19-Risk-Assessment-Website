// Global parameters: do not resize the chart canvas
Chart.defaults.global.responsive = false;
Chart.defaults.global.animation.duration = 3000;

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




