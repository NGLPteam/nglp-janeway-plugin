# NGLP Janeway events

Janeway has an events framework in [src/events/logic.py](https://github.com/BirkbeckCTP/janeway/blob/master/src/events/logic.py) which
provides an easy way to add custom functionality when things happen.

Event listeners are registered by adding them to `plugin_settings.py` in a `register_for_events()` method
(see [the typesetting plugin](https://github.com/BirkbeckCTP/typesetting/blob/master/plugin_settings.py#L70) for an example):

```python
def register_for_events():
    # Plugin modules can't be imported until plugin is loaded
    from plugins.typesetting.notifications import emails

    events_logic.Events.register_for_event(
        ON_TYPESETTING_ASSIGN_NOTIFICATION,
        emails.send_typesetting_assign_notification,
    )
```


## Request and Investigation events

These occur, respectively, when a user downloads and views an article. In Janeway, these are handled by the `download_galley` and `view_galley` views.
Janeway are adding a new `ON_ARTICLE_ACCESS` event for this in https://github.com/BirkbeckCTP/janeway/pull/2363.


## Workflow transition events

These are already covered by various existing events. We have chosen the workflow events that we are currently 
interested in: when an article is submitted, reviewed, accepted and published. In Janeway, these are handled by the 
```submission```, ```review``` and ```journal``` views. We are using the ```ON_ARTICLE_SUBMITTED```, 
```ON_REVIEW_COMPLETE```, ```ON_ARTICLE_ACCEPTED```, and ```ON_ARTICLE_PUBLISHED``` events.


## Export events

We're going to skip these, as I don't think Janeway has an export for reference managers.

Question: Unless we want to attach this to the JATS XML export?


## Join and Leave events

These aren't available via Janeway events, but we can attach to Django post_save and pre_delete signals on `AccountRole` model objects. `AccountRole`
represents a relationship between a user and a journal, with types such as "author", "editor", "reviewer", "copyeditor", "production", "typesetter".

Question: Do we know which roles we care about?
