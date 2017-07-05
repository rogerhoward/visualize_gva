$( document ).ready(function() {
    console.log( "ready2!" );

    $.get( "data.json", function( data ) {
        console.log(data);
        lineGraph(data);
    });

});


function lineGraph(data) {
    console.log('starting');
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