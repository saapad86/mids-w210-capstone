
# This class is responsible for generating Highcharts Javascript
class ChartGenerator(Object):
	def __init__(self,**kwargs):
		self.js = ''
		self.container = kwargs['container'] if 'container' in kwargs.keys() else 'container'

	def defaultTitle(self):
		self.title = """
			title: {
				text: 'Untitled'
			}
		"""

class LineChart(ChartGenerator):
	def __init__(self,**kwargs):
		super().init(**kwargs)

	def generate(self):
		option_list = ['container','title','yAxis','legend','plotOptions','series','responsive']
		options = dict(zip(option_list,[getattr(self,o) for o in option_list]))
		self.js = """
			Highcharts.chart('{container}', {
				{title},
				{subtitle},
				{yAxis},
				{legend},
				{plotOptions},
				{series},
				{responsive},
			});
		""".format(**options)

		return self.js




Highcharts.chart('container', {

    title: {
        text: 'Solar Employment Growth by Sector, 2010-2016'
    },

    subtitle: {
        text: 'Source: thesolarfoundation.com'
    },

    yAxis: {
        title: {
            text: 'Number of Employees'
        }
    },
    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'middle'
    },

    plotOptions: {
        series: {
            label: {
                connectorAllowed: false
            },
            pointStart: 2010
        }
    },

    series: [{
        name: 'Qualified Delivery',
        data: {{data1|safe}}
    }],

    responsive: {
        rules: [{
            condition: {
                maxWidth: 500
            },
            chartOptions: {
                legend: {
                    layout: 'horizontal',
                    align: 'center',
                    verticalAlign: 'bottom'
                }
            }
        }]
    }

});