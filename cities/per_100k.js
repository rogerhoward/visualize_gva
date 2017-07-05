$( document ).ready(function() {
    console.log( "ready2!" );

    $.get( "./cities.json", function( data ) {
        showCities(data);
    });

    $.get( "./data_per_100k/NA.json", function( data ) {
        lineGraph(data);
    });

});


function showCities(data) {
    console.log('starting showCities');
    var list = $("#citySelect");
    $.each( data.cities, function( key, value ) {
        if (value.code == 'NA') {
            list.append('<option value="'+value.code+'" selected>' + value.name + '</option>');
        } else {
            list.append('<option value="'+value.code+'">' + value.name + '</option>');
        }
    });
}

function changeCity(theOption) {
    $.get( "data_per_100k/"+ theOption.value +".json", function( data ) {
        lineGraph(data);
    });
}

function lineGraph(data) {
    console.log('graphing...');
    var ctx = $("#myChart");

    var myChart = new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        }
    });
}