## Actions Macro

### Parameters

None

### Examples

    <div class='macro macro_dashboard'>
    {
      "columns": [
        {
          "order": 0,
          "widgets": [
            {"order": 0, "id": "widget1", "widgettype": "include", "title": "Widget 1", "config": {"name": "Home"}},
            {"order": 1, "id": "widget2", "widgettype": "actions", "title": "Actions", "config": {}}
          ]
        },
        {
          "order": 1,
          "widgets": [
            {"order": 0, "id": "widget3", "widgettype": "include", "title": "Widget 3", "config": {"name": "Macros"}},
            {"order": 1, "id": "widget4", "widgettype": "youtube", "title": "Monty Python", "config": {}}
          ]
        }
      ], 
      "id": "dashboard1", 
       "title": "My Dashboard"
    }
    </div>

---

<div class="macro macro_dashboard">
{
    "columns": [
      {
        "order": 0,
        "widgets": [
          {"order": 0, "id": "widget1", "widgettype": "include", "title": "Widget 1", "config": {"name": "Home"}},
          {"order": 1, "id": "widget2", "widgettype": "actions", "title": "Actions", "config": {}}
        ]
      },
      {
        "order": 1,
        "widgets": [
          {"order": 0, "id": "widget3", "widgettype": "include", "title": "Widget 3", "config": {"name": "Macros"}},
          {"order": 1, "id": "widget4", "widgettype": "youtube", "title": "Monty Python", "config": {}}
        ]
      }
    ], 
    "id": "dashboard1", 
    "title": "My Dashboard"
}
</div>

---

