$( document ).ready(function() {
    console.log( "ready2!" );

    $.get( "diff.json", function( data ) {
        console.log(data);
        lineGraph(data);
    });

});


function lineGraph(data) {
    console.log('starting');
    var ctx = $("#myChart");

    var myChart = new Chart(ctx, {
        type: 'bar',
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