function dstPortGraph(data) {
  var in_port = Object.keys(data.ibyt);
  var in_bytes = Object.values(data.ibyt);
  var out_port = Object.keys(data.obyt);
  var out_bytes = Object.values(data.obyt);

  new Chart(document.getElementById("inBytesDstPort"), {
    type: 'doughnut',
    data: {
      labels: in_port,
      datasets: [
        {
          label: "Number of bytes sent",
          backgroundColor: colour_generator(in_port.length),
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
        text: 'Bytes sent to destination ports'
      }
    }
  });

  new Chart(document.getElementById("outBytesDstPort"), {
    type: 'doughnut',
    data: {
      labels: out_port,
      datasets: [
        {
          label: "Number of bytes recieved",
          backgroundColor: colour_generator(out_port.length),
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
        text: 'Bytes recieved from destination ports'
      }
    }
  });
}
