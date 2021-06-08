// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Pie Chart Example
var ctx = document.getElementById("myPieChart");
var myPieChart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ["Azadpur", "Shalimar Bagh", "NSP", "Naraina Vihar"],
    datasets: [{
      data: [azppendcount, slmpendcount, nsppendcount, naipendcount],
      backgroundColor: ['#4e73df', '#1cc88a', '#ff8000', "#ffff00"],
      hoverBackgroundColor: ['#2e59d9', '#17a673', '#cc7a00', '#cccc00'],
      hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
  },
  options: {
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 2,
      xPadding: 15,
      yPadding: 15,
      displayColors: true,
      caretPadding: 10,
    },
    legend: {
      display: true,
      position: 'bottom',
    },
    cutoutPercentage: 70,
  },
});
