# Pseudo classes and states

## hover, focus

```html
<button class="bg-violet-500 hover:bg-violet-600 active:bg-violet-700 focus:outline-none focus:ring focus:ring-violet-300 ...">
  Save changes
</button>
```

## first, last

```html
<ul role="list" class="p-6 divide-y divide-slate-200">
  {#each people as person}
    <!-- Remove top/bottom padding when first/last child -->
    <li class="flex py-4 first:pt-0 last:pb-0">
      <img class="h-10 w-10 rounded-full" src="{person.imageUrl}" alt="" />
      <div class="ml-3 overflow-hidden">
        <p class="text-sm font-medium text-slate-900">{person.name}</p>
        <p class="text-sm text-slate-500 truncate">{person.email}</p>
      </div>
    </li>
  {/each}
</ul>
```

## odd, even

```html
<table>
  <!-- ... -->
  <tbody>
    {#each people as person}
      <!-- Use a white background for odd rows, and slate-50 for even rows -->
      <tr class="odd:bg-white even:bg-slate-50">
        <td>{person.name}</td>
        <td>{person.title}</td>
        <td>{person.email}</td>
      </tr>
    {/each}
  </tbody>
</table>
```

>Note: [Complete reference for modifiers and pseudo class references](https://tailwindcss.com/docs/hover-focus-and-other-states#pseudo-class-reference)

##  required, invalid, and disabled

```html
<form>
  <label class="block">
    <span class="block text-sm font-medium text-slate-700">Username</span>
    <!-- Using form state modifiers, the classes can be identical for every input -->
    <input type="text" value="tbone" disabled class="mt-1 block w-full px-3 py-2 bg-white border border-slate-300 rounded-md text-sm shadow-sm placeholder-slate-400
      focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500
      disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none
      invalid:border-pink-500 invalid:text-pink-600
      focus:invalid:border-pink-500 focus:invalid:ring-pink-500
    "/>
  </label>
  <!-- ... -->
</form>
```

## Groups

```html
<a href="#" class="group block max-w-xs mx-auto rounded-lg p-6 bg-white ring-1 ring-slate-900/5 shadow-lg space-y-3 hover:bg-sky-500 hover:ring-sky-500">
  <div class="flex items-center space-x-3">
    <svg class="h-6 w-6 stroke-sky-500 group-hover:stroke-white" fill="none" viewBox="0 0 24 24"><!-- ... --></svg>
    <h3 class="text-slate-900 group-hover:text-white text-sm font-semibold">New project</h3>
  </div>
  <p class="text-slate-500 group-hover:text-white text-sm">Create a new project from a variety of starting templates.</p>
</a>
```

### Nested groups

When nesting groups, you can style something based on the state of a specific parent group by giving that parent a unique group name using a `group/{name}` class, and including that name in modifiers using classes like `group-hover/{name}`:

```html
<ul role="list">
  {#each people as person}
    <li class="group/item hover:bg-slate-100 ...">
      <img src="{person.imageUrl}" alt="" />
      <div>
        <a href="{person.url}">{person.name}</a>
        <p>{person.title}</p>
      </div>
      <a class="group/edit invisible hover:bg-slate-200 group-hover/item:visible ..." href="tel:{person.phone}">
        <span class="group-hover/edit:text-gray-700 ...">Call</span>
        <svg class="group-hover/edit:translate-x-0.5 group-hover/edit:text-slate-500 ...">
          <!-- ... -->
        </svg>
      </a>
    </li>
  {/each}
</ul>
```
`group-hover/item` means that on `hover` of `group` `item`, make this element `visible`

### Arbitary group based on criteria

```html
<div class="group is-published">
  <div class="text-blue-600 group-[.is-published]:text-red-600">
    Published
  </div>
</div>
```
if parent `group` has `is_published` class on it, make this element colored red else blue

### Style based on Sibling state

```html
<form>
  <label class="block">
    <span class="block text-sm font-medium text-slate-700">Email</span>
    <input type="email" class="peer ..."/>
    <p class="mt-2 invisible peer-invalid:visible text-pink-600 text-sm">
      Please provide a valid email address.
    </p>
  </label>
</form>
```

if `peer` is `invalid`, make this element `visible`. This only works if `peer` is a previous element

Peers also work with arbitary selection criteria like groups.

```html
<form>
  <label for="email">Email:</label>
  <input id="email" name="email" type="email" class="is-dirty peer" required />
  <div class="peer-[.is-dirty]:peer-required:block hidden">This field is required.</div>
  <!-- ... -->
</form>
```

## After and Before

```html
<form>
  <label for="email">Email:</label>
  <input id="email" name="email" type="email" class="is-dirty peer" required />
  <div class="peer-[.is-dirty]:peer-required:block hidden">This field is required.</div>
  <!-- ... -->
</form>
```

## Placeholder text styling

```html
<label class="relative block">
  <span class="sr-only">Search</span>
  <span class="absolute inset-y-0 left-0 flex items-center pl-2">
    <svg class="h-5 w-5 fill-slate-300" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"></path>
    </svg>
  </span>
  <input class="placeholder:italic placeholder:text-slate-400 block bg-white w-full border border-slate-300 rounded-md py-2 pl-9 pr-3 shadow-sm focus:outline-none focus:border-sky-500 focus:ring-sky-500 focus:ring-1 sm:text-sm" placeholder="Search for anything..." type="text" name="search"/>
</label>
```

## Misc

**List Markers**: To style bullets of list
```html
<ul role="list" class="marker:text-sky-400 list-disc pl-5 space-y-3 text-slate-400">
  <li>5 cups chopped Porcini mushrooms</li>
  <li>1/2 cup of olive oil</li>
  <li>3lb of celery</li>
</ul>
```

**Selection styling**: How selected should look like
```html
<div class="selection:bg-fuchsia-300 selection:text-fuchsia-900">
  <p>
    So I started to walk into the water. I won't lie to you boys, I was
    terrified. But I pressed on, and as I made my way past the breakers
    a strange calm came over me. I don't know if it was divine intervention
    or the kinship of all living things but I tell you Jerry at that moment,
    I <em>was</em> a marine biologist.
  </p>
</div>
```

**First Line and First letter styling**
```html
<p class="first-line:uppercase first-line:tracking-widest
  first-letter:text-7xl first-letter:font-bold first-letter:text-white
  first-letter:mr-3 first-letter:float-left
">
  Well, let me tell you something, funny boy. Y'know that little stamp, the one
  that says "New York Public Library"? Well that may not mean anything to you,
  but that means a lot to me. One whole hell of a lot.
</p>
```

**Viewport orientation**

`portait:` & `landscape:`

**Print**

`print` Only on printing


# Dark mode

Use `dark:` for properties in dark mode

```html
<div class="bg-white dark:bg-slate-900 rounded-lg px-6 py-8 ring-1 ring-slate-900/5 shadow-xl">
  <div>
    <span class="inline-flex items-center justify-center p-2 bg-indigo-500 rounded-md shadow-lg">
      <svg class="h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true"><!-- ... --></svg>
    </span>
  </div>
  <h3 class="text-slate-900 dark:text-white mt-5 text-base font-medium tracking-tight">Writes Upside-Down</h3>
  <p class="text-slate-500 dark:text-slate-400 mt-2 text-sm">
    The Zero Gravity Pen can be used to write in any orientation, including upside-down. It even works in outer space.
  </p>
</div>
```

# Responsive design

To style an element at a specific breakpoint, use responsive modifiers like md and lg.

For example, this will render a 3-column grid on mobile, a 4-column grid on medium-width screens, and a 6-column grid on large-width screens:

```html
<div class="grid grid-cols-3 md:grid-cols-4 lg:grid-cols-6">
  <!-- ... -->
</div>
```


Prefix	    Minimum width   CSS
sm	        640px	        @media (min-width: 640px) { ... }
md	        768px	        @media (min-width: 768px) { ... }
lg	        1024px	        @media (min-width: 1024px) { ... }
xl	        1280px	        @media (min-width: 1280px) { ... }
2xl	        1536px	        @media (min-width: 1536px) { ... }

## Mobile first design

Always design the default style of mobile and then add identifiers for the rest of the break points

```html
<!-- This will center text on mobile, and left align it on screens 640px and wider -->
<div class="text-center sm:text-left"></div>
```

# Custom mixing css types

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer components {
  .btn-primary {
    @apply py-2 px-4 bg-blue-500 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-opacity-75;
  }
}
```
This applies extra CSS rules on the CSS class `btn-primary`

**Apply CSS and use modifiers with custom CSS**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer utilities {
  .content-auto {
    content-visibility: auto;
  }
}
```

```html
<div class="lg:dark:content-auto">
  <!-- ... -->
</div>
```

## Using arbitary values

```html
<div class="top-[117px] lg:top-[344px]">
  <!-- ... -->
</div>
```

use `-[]` to define arbitary values

# Layouts

## Container

Doesn't center itself, so use `mx-auto`

```html
<div class="container mx-auto">
<!-- ... -->
</div>
```

### Columns based layout

This is for book like columns layouts

**Col 4 with 7 elements will be like**

1   3   5   7
2   4   6

If columns 1 is very large, it will spill over like below (like a book()

1.1     1.5     3   7
1.2     1.6     4
1.3     1.7     5
1.4     2       6

```html
<div class="columns-4 ...">
  <div class="w-full m-4 bg-red-500"/>1</div>
  <div class="w-full m-4 bg-red-500"/>2</div>
  <div class="w-full m-4 bg-red-500"/>3</div>
  <div class="w-full m-4 bg-red-500"/>4</div>
  <div class="w-full m-4 bg-red-500"/>5</div>
  <div class="w-full m-4 bg-red-500"/>6</div>
  <div class="w-full m-4 bg-red-500"/>7</div>
</div>
```

# Flex layout

### Basics of CSS first:

Always inside a `container` which defines `display:flex` in CSS. The following properties are allowed in the `container`


- `flex-direction` tell the flow of elements will be in column-axis(Vertical) or row-axis(Horizontal, **Default**). Value allowed `column`, `row`, `column-reversed`, `row-reversed`
- `justify-content` defines **main-axis alignment** (for `row` it will justify along **X-axis**). Values are:
    - `flex-start` (aligned where it starts)
    - `flex-end` (aligned where it ends)
    - `space-between` (distributed equally, with first and last elements are at the start and end)
    - `space-around` (distributed equally such that start and end are also spaced out)
    - `space-evenly` (distributed equally such that start and end are treated as elements too, looks more even)
- `align-item` defined the **orthogonal-axis** alignment (for `row` it will justify along **Y-axis**). Values are:
  - `flex-start`: Align from the start (for `row` its aligned at the **top**)
  - `flex-bottom`: Align along the end (for `row` its aligned at the **bottom**)
  - `center`: Align along the center (center align vertically)
  - `baseline`: Align such that baseline is aligned for first element inside the elements
- `place-content` to place the content across main and cross axis
  -`place-content-center` to place all content in the center horizontally and vertically
  -`place-content-start` to palce all content at the start (0,0)
  -`place-content-end` to place all content at the end
  -`place-content-between`
  -`place-content-around`
  -`place-content-evenly`
  -`place-content-baseline`

- `flex-wrap`: By default `nowrap`, so everything fits in the same row, with `wrap` if space it not present it wraps. Behaves exactly like text wrap.
- `align-content`: ONLY WORKS WITH `wrap`. Equivalent of `justify-content` in case of `wrap`
- `gap`: allows for gap between elements.

If you want elements inside the container to have different behaviour, apply the following to the items:
- `flex-grow`: If there is space left (`justify-content` is either `flex-start` or `flex-end`). Then applying `flex-grow:1` will get that item to take the remaining space.
- `flex-shrink`: During resizing to smaller screen, this property on any item will not allow item to shrink if set to `flex-shrink:0`, else it will shrink that item according to the value.
- `flex-basis`: Overrides the width of the item, if set to `flex-basis:0`, this will shrink
- `flex`: This is the combination of the above 3 properties

### Flex in tailwind

- `flex-basis`: Tailwind provides `basis-0, basis-1... basis-96` to manage width of elements in `rem` units. Or `basis-1/2, basis-1/3, basis-4/12, basis-7/12` for percentage values
- `flex-direction`: Tailwind values `flex-row`, `flex-col`, `flex-row-reverse`, `flex-col-reverse`
- `flex-wrap`: `flex-wrap`, `flex-nowrap`, `flex-wrap-reverse`
- For flex grow and shrink:
  - `flex-initial` to allow a flex item to shrink but not grow, taking into account its initial size
  - `flex-1` to allow a flex item to grow and shrink as needed, ignoring its initial size
  - `flex-auto` to allow a flex item to grow and shrink, taking into account its initial size
  - `flex-none` to prevent a flex item from growing or shrinking
- Initial size:
  - `grow` to allow a flex item to grow to fill any available space
  - `grow-0` to prevent a flex item from growing
  - `shrink` to allow a flex item to shrink if needed
  - `shrink-0` to prevent a flex item from shrinking:
- Justify content using `justify-normal` `justify-start` `justify-end` `justify-center` `justify-between` `justify-around` `justify-evenly` `justify-stretch`
- Align content (across cross axis) using `content-normal` `content-center` `content-start` `content-end` `content-between` `content-around` `content-evenly` `content-baseline` `content-stretch`
- `place-content-{position}` to place it vertically and horizontally like `place-content-{position}` in regular flex design

## Grid layouts

To define a grid of 4 columns with a gap of 4:

01  02  03  04
05  06

```html
<div class="grid grid-cols-4 gap-4">
  <div class="bg-red-600">01</div>
  <div class="bg-red-600">02</div>
  <div class="bg-red-600">03</div>
  <div class="bg-red-600">04</div>
  <div class="bg-red-600">05</div>
  <div class="bg-red-600">06</div>
</div>
```
To specify grid in the `rows` use `grid-row-{n} grid-flow-col`

### Grid element layout

- `col-span-{n}` to tell the element to occupy `n` spans. If it doesn't fit, the entire element wraps down
- `col-start-{m} col-end-{n}` to tell the element to start from column `m` and end at column `n`
- `row-span-{n}` to occupy `n` span across row layout
- `row-start-{m}` to `row-end-{n}` to start element from `m` to `n` row

