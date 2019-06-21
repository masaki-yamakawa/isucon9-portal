(function() {
    var labelColors = [
        [244,67,54],
        [233,30,99],
        [156,39,176],
        [103,58,183],
        [63,81,181],
        [33,150,243],
        [3,169,244],
        [0,188,212],
        [0,150,136],
        [76,175,80],
        [139,195,74],
        [205,220,57],
        [255,235,59],
        [255,193,7],
        [255,152,0],
        [255,87,34],
        [121,85,72],
        [158,158,158],
        [96,125,139],

        [239,83,80],
        [236,64,122],
        [171,71,188],
        [126,87,194],
        [92,107,192],
        [66,165,245],
        [41,182,246],
        [38,198,218],
        [38,166,154],
        [102,187,106],
        [156,204,101],
        [212,225,87],
        [255,238,88],
        [255,202,40],
        [255,167,38],
        [255,112,67],
        [141,110,99],
        [189,189,189],
        [120,144,156],

        [229,115,115],
        [240,98,146],
        [186,104,200],
        [149,117,205],
        [121,134,203],
        [100,181,246],
        [79,195,247],
        [77,208,225],
        [77,182,172],
        [129,199,132],
        [174,213,129],
        [220,231,117],
        [255,241,118],
        [255,213,79],
        [255,183,77],
        [255,138,101],
        [161,136,127],
        [224,224,224],
        [144,164,174],
    ];

    var ctx = $("#myChart");
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: JSON.parse('<: $chart_data.labels | json :>'),
            datasets: [
                : for $chart_data.list -> $row {
                {
                    label: '<: $row.team.name :> (<: $row.team.id :>)',
                    data: JSON.parse('<: $row.scores | json :>'),
                    lineTension: 0,
                    backgroundColor: 'rgba(' + labelColors[ <: $~row :> % (labelColors.length - 1) ].join(',')  + ',1)',
                    borderColor: "rgba(" + labelColors[ <: $~row :> % (labelColors.length - 1) ].join(',')  + ',1)',
                    borderWidth: 2,
                    fill: false,
                    pointHoverRadius: 4,
                    pointRadius: 2,
                    spanGaps: true,
                },
                : }
            ],
        },
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
})()