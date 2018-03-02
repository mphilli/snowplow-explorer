window.onload = set_values();

window.loadsession = function(sess, marker) {
            if (marker == true) {
                base = "/session/markers/";
            } else {
                base = "/session/"
            }
        var pathArray = location.href.split("/");
        var base_url = pathArray[0] + "//" + pathArray[2] + "/";
        if (pathArray.length > 3) {
			var date = pathArray[4];
			if (date == "markers") {
			    location.href = "/session/" + pathArray[5];
			} else if (!isNaN(date)) {
			    location.href = "/session/" + pathArray[4];
			} else {
			var start = pathArray[5];
			var end = pathArray[6];
			var url = base + sess + "/from";
            url = url + date + "D" + start + "T" + end + "S";
            if (pathArray.length > 7) {
            	url = url + pathArray[7];
            }
            location.href = url;
            }
        } else {
        	location.href = base + sess;
        }

}


function set_values() {
    var pathArray = location.href.split("/");
    var protocol = pathArray[0]; // don't need this
    var host = pathArray[2];
    var base_url = protocol + "//" + host + "/";
    var query_type = pathArray[3];
    if (query_type == "interval") {
        var date = pathArray[4];
        var start = pathArray[5];
        var end = pathArray[6];
        set_date(date);
        document.getElementById("start").value = start.replace(/-/g, ":");
        document.getElementById("end").value = end.replace(/-/g, ":");
    }
}

function process_from() {
    var last_value = location.href.split("/")[location.href.split("/").length - 1];
    // ex: from2018-03-13D00-00-00T06-00-00Sjames
    if (last_value.startsWith("from")) {
        last_value = last_value.replace("from", "");
        var date = last_value.split("D")[0];
        var start = last_value.split("D")[1].split("T")[0];
        var end = last_value.split("D")[1].split("T")[1].split("S")[0];
        var street = last_value.split("S")[1];
        // Next, let's create a new URL to visit.
        var pathArray = location.href.split("/");
        var protocol = pathArray[0]; // don't need this
        var host = pathArray[2];
        var base_url = protocol + "//" + host + "/";
        url = base_url + "interval/" + date + "/" + start + "/" + end + "/" + street.toLowerCase();
        location.href = url;
    }
}

function set_date(date_in) {
    var val = date_in.replace(/-/g, "/");
    var select = document.getElementById("date-select");
    for (var i = 0; i < select.options.length; i++) {
        if (select.options[i].value == val) {
        select.selectedIndex = i;
        break;
        }
    }
}

function load_data() {
    // First, let's grab data from each of the fields. This will make up our new URL.
    var e = document.getElementById("date-select");
    var date = e.options[e.selectedIndex].value.replace(/[/]/g, "-");

    var start = document.getElementById("start").value
    if (start != "") {
        start = start.replace(/:/g, "-");
    } else {
        start = "00-00-00"; // default value if empty
    }

    var end = document.getElementById("end").value.replace(/:/g, "-");
    if (end != "") {
        end = end.replace(/:/g, "-");
    } else {
        end = "06-00-00"; // default value if empty
    }


    var street = document.getElementById("street").value;
    if (street == null) {
        street = "";
    }

    // Next, let's create a new URL to visit.
    var pathArray = location.href.split("/");
    var protocol = pathArray[0]; // don't need this
    var host = pathArray[2];
    var base_url = protocol + "//" + host + "/";
    url = base_url + "interval/" + date + "/" + start + "/" + end + "/" + street.toLowerCase();
    location.href = url;
}

function filterTable() {

  var input = document.getElementById("data-filter");
  var filter = input.value.toLowerCase();
  var table = document.getElementById("session-table");
  var tr = table.getElementsByTagName("tr");

  // Loop through rows
  for (var i = 0; i < tr.length; i++) {
    var address = tr[i].getElementsByTagName("td")[4]; // grab address column
    if (address) {
      var activity = tr[i].getElementsByTagName("td")[5];
      if (activity) {
        var act = activity.innerHTML.toLowerCase();
      } else {
        var act = ""; // no activity for this row
      }
      // search street and activity, prioritizing street
      street_act = address.innerHTML.toLowerCase() + act;
      if (filter.split(" ").every(function(i) {
        return street_act.includes(i);})) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

function downloadCSV(csv, filename) {
    // courtesy of https://www.codexworld.com/export-html-table-data-to-csv-using-javascript/
    var csvFile;
    var downloadLink;

    // CSV file
    csvFile = new Blob([csv], {type: "text/csv"});

    // Download link
    downloadLink = document.createElement("a");

    // File name
    downloadLink.download = filename;

    // Create a link to the file
    downloadLink.href = window.URL.createObjectURL(csvFile);

    // Hide download link
    downloadLink.style.display = "none";

    // Add the link to DOM
    document.body.appendChild(downloadLink);

    // Click download link
    downloadLink.click();
}

function exportTableToCSV(filename) {
    // courtesy of https://www.codexworld.com/export-html-table-data-to-csv-using-javascript/
    var csv = [];
    var rows = document.querySelectorAll("table tr");

    for (var i = 0; i < rows.length; i++) {
        var row = [], cols = rows[i].querySelectorAll("td, th");

        for (var j = 0; j < cols.length; j++)
            row.push(cols[j].innerText);

        csv.push(row.join(","));
    }

    // Download CSV file
    downloadCSV(csv.join("\n"), filename);
}
