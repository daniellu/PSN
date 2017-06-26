---
title: Hello World!
---

<h2>Results of Craiglist Spider</h2>


<table>
    <thead>
        <tr>
            <th>Title</th>
            <th>Price</th>
            <th>Post Date</th>
            <th>Link</th>
        </tr>
    </thead>
    <tbody>
    {% for post in site.data.craigslist %}    
        <tr>
            <td>{{ post.title }}</td>
            <td>{{ post.price }}</td>
            <td>{{ post.post_date }}</td>
            <td><a href="{{ post.url }}">View</a></td>
        </tr>
    {% endfor %}
    </tbody>
</table>