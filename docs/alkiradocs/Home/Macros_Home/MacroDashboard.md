@metadata title=Dashboard Macro
@metadata tagstring=macro alkira dashboard

[imgInitialDashboard]: images/images50/md_images/initialDashboard.png
[configureDashboard]: images/images50/md_images/configureDashboard.png
[addWidget]: images/images50/md_images/addWidget.png
[configureWidget]: images/images50/md_images/configureWidget.png

#Dashboard Macro
The `dashboard` macro allows you to create a page to which you can add widgets. This way you can create a custom page with your favorite widgets.


##Adding the Dashboard Macro

To add the Dashboard macro to a page, simply add the following line to your page:

    [[dashboard:config=myconfig]][[/dashboard]]
    
The name of the `config` parameter can be freely chosen, but a name is mandatory. 

From then on you have to configure your dashboard through the Alkira documentation. Go to your page where you have created your dashboard. An empty dashboard looks like this:

![InitialDashboard][imgInitialDashboard]


##Configuring the Dashboard

To configure your dashboard, click the wrench icon in the top right-hand corner of the dashboard area.

![configureDashboard][configureDashboard]

* Title: set a name for your dashboard
* Number of columns: set the number of columns that will be shown in your dashboard


##Adding Widgets to Dashboard

To add widgets to the dashboard, click the 'plus' icon in the top right-hand corner of the dashboard area.

![addWidget][addWidget]

Click `Pick me` next to the desired widget to add it to your dashboard. A configuration window for your widget appears. This window is widget dependent.
Below you find an example for the Google Maps macro.

![configureWidget][configureWidget]


##Post-Configuration of a Dashboard
When you want to rearrange your widgets, drag and drop the widgets to the desired location in the dashboard. Click in the title bar of the widget to grab the widget.
