$(function () {
  console.log("ready!");

  grafico();
});

function grafico() {

  var data = {
    labels: dias,
    datasets: [
      {
        label: "Género Masculino",
        data: genero_masculino,
        backgroundColor: 'blue',
        borderColor: 'blue',
        borderWidth: 1
      },
      {
        label: "Género Femenino",
        data: genero_femenino,
        backgroundColor: 'green',
        borderColor: 'green',
        borderWidth: 1

      }
    ]
  };
  var ctx = $("#accionChart");
  var myChart = new Chart(ctx, {
    type: 'bar',
    data: data,
    options: {
      title: {
        display: true,
        fontStyle: 'bold',
        text: "Pacientes por Especialidad"
      },
      legend: {
        position: "bottom",
        labels: {}
      },
      tooltips: {
        mode: 'label',
        bodySpacing: 10,
        cornerRadius: 0,
        titleMarginBottom: 15,
        callbacks: {
          label: function (tooltipItem, data) {
            return "Pacientes por género: " + Number(tooltipItem.yLabel).toFixed(0).replace(/./g, function (c, i, a) {
              return i > 0 && c !== "," && (a.length - i) % 3 === 0 ? "." + c : c;
            });
          }
        }
      },
      scales: {
        xAxes: [{
          ticks: {}
        }],
        yAxes: [{
          ticks: {
            min: 0, // it is for ignoring negative step.
            beginAtZero: true,
            callback: function (value, index, values) {
              if (Math.floor(value) === value) {
                value = value.toString();
                value = value.split(/(?=(?:...)*$)/);

                // Convert the array to a string and format the output
                value = value.join('.');
                return value;
              }
            }

          }
        }]
      },
      responsive: true
    }
  });

}