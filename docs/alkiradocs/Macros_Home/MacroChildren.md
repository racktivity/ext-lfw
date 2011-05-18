# Children Macro
The `children` macro creates a tree-view of a certain page and all its chilkd pages.


##Parameters

* **depth**: integer that indicates how many levels deep you want to show the child pages.
* **root**: optional, name of the page whose child pages you want to show. If not provided, all pages of the space will be taken into account


##Example
Assuming we want to show the children of the `Macros_Home` page, we would add:

    [[children]]depth:2, root:Macros_Home[[/children]]


##Sample

[[children]]depth:2, root:Macros_Home[[/children]]
