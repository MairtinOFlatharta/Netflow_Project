function bytesGraphs(data, descriptions) {
  var in_keys = Object.keys(data.ibyt);
  var in_bytes = Object.values(data.ibyt);
  var out_keys = Object.keys(data.obyt);
  var out_bytes = Object.values(data.obyt);

  var colours = colour_generator(in_keys.length);

  new Chart(document.getElementById("inBytesCanvas"), {
    type: 'doughnut',
    data: {
      labels: in_keys,
      datasets: [
        {
          label: "Number of bytes sent",
          backgroundColor: colours,
          data: in_bytes
        }
      ]
    },
    options: {
      responsive: false,
      maintainAspectRation: true,
      animation: {
        animateScale: true
      },
      title: {
        display: true,
        text: descriptions[0]
      }
    }
  });

  new Chart(document.getElementById("outBytesCanvas"), {
    type: 'doughnut',
    data: {
      labels: out_keys,
      datasets: [
        {
          label: "Number of bytes recieved",
          backgroundColor: colours,
          data: out_bytes
        }
      ]
    },
    options: {
      responsive: false,
      maintainAspectRation: true,
      animation: {
        animateScale: true
      },
      title: {
        display: true,
        text: descriptions[1]
      }
    }
  });
}
