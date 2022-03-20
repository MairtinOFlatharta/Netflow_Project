function bytesGraphs(in_data, out_data, descriptions) {
  var in_keys = Object.keys(in_data);
  var in_bytes = Object.values(in_data);
  var out_keys = Object.keys(out_data);
  var out_bytes = Object.values(out_data);

  var in_colours = colour_generator(in_keys.length);
  var out_colours = colour_generator(out_keys.length);

  new Chart(document.getElementById("inBytesCanvas"), {
    type: 'doughnut',
    data: {
      labels: in_keys,
      datasets: [
        {
          label: "Number of bytes sent",
          backgroundColor: in_colours,
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
        text: "Top " + in_keys.length + " " + descriptions[0]
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
          backgroundColor: out_colours,
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
        text: "Top " + out_keys.length + " " + descriptions[1]
      }
    }
  });
}
