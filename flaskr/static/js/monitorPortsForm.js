var headers = ["", "Communication Protocol", "Port Number"];
var portTable = document.getElementById("portTable");
var tbody = portTable.getElementsByTagName('tbody')[0];
var buttonHTML = '<td><input type="button" value="Remove" onclick="deleteRow(this)" class="btn btn-warning" /></td>';
var dropdownSelectHTML = `<td>
                            <select name="portOptions">
                              <option value="TCP">TCP</option>
                              <option value="UDP">UDP</option>
                              <option value="ICMP">ICMP</option>
                              <option value="IGMP">IGMP</option>
                            </select>
                          </td>`;
var inputHTML = '<td><input type="number" class="form-control" /></td>';

function addRow(){
  // Get number of rows
  var rowCount = tbody.rows.length;

  // Get reference to new row
  var tr = tbody.insertRow(rowCount);

  // Insert html into row
  tr.innerHTML = buttonHTML + dropdownSelectHTML + inputHTML;
}

function deleteRow(oButton){
  // Delete row where the clicked button is located
  tbody.deleteRow(oButton.parentNode.parentNode.rowIndex - 1);
}

function portSubmit(){
  var values = new Array();
  // Loop through all rows of table
  for(row = 0; row < tbody.rows.length; row++){
    // Get protocol of select field (TCP, UDP etc)
    var protocol = tbody.rows.item(row).cells[1].childNodes[1].value;
    // Get port number from number input
    var portNum = parseInt(tbody.rows.item(row).cells[2].childNodes[0].value);
    values.push([protocol, portNum]);
  }
  // Insert values into hidden field in form
  document.portForm.ports.value = JSON.stringify(values);
}
