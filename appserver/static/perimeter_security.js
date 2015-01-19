require([
	'underscore',
	'jquery',
	'splunkjs/mvc',
	'splunkjs/mvc/tableview',
	'splunkjs/mvc/simplexml/ready!'
], function(_, $, mvc, TableView) {
	 // Row Coloring Example with custom, client-side range interpretation
	var HomeSecurityZoneCellRenderer = TableView.BaseCellRenderer.extend({
		canRender: function(cell) {
			return true; 
		},
		render: function($td, cell) {
			var boxClass = "zone_open";
			if(cell.value.toLowerCase() === "closed") {
				boxClass = "zone_closed";
			} else {
				boxClass = "zone_open";
			}

			$td.html(
				'<div class="zone_statusbox '+boxClass+'"><span class="zone_title">'
				+ cell.field +
				'</span><span class="zone_statustext">'
				+ cell.value +
				'</span></div>'
			);
		}
	});

	var HomeSecuritySystemCellRenderer = TableView.BaseCellRenderer.extend({
		canRender: function(cell) {
			return true; 
		},
		render: function($td, cell) {
			var boxClass = "zone_open";
			var boxText = "Security System Disarmed";
			if(cell.value.toLowerCase() === "enabled") {
				boxClass = "system_armed";
				boxText = "Security System Armed";
			} else {
				boxClass = "system_disarmed";
				boxText = "Security System Disarmed";
			}

			$td.html(
				'<div class="zone_statusbox '+boxClass+'"><span class="zone_statustext">'
				+ boxText +
				'</span></div>'
			);
		}
	});




	mvc.Components.get('zone_status').getVisualization(function(tableView) {
		tableView.table.addCellRenderer(new HomeSecurityZoneCellRenderer());
		tableView.table.render();
	});

	mvc.Components.get('system_status').getVisualization(function(tableView) {
		tableView.table.addCellRenderer(new HomeSecuritySystemCellRenderer());
		tableView.table.render();
	});



});

