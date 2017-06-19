Hello World!

Result of Craiglist
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
    {% for post_hash in site.data.craigslist %}
    {% assign post = post_hash[1] %}
        <tr>
            <td>{{ post.title }}</td>
            <td>{{ post.price }}</td>
            <td>{{ post.post_date }}</td>
            <td><a href="{{ post.url }}">View</a></td>
        </tr>
    {% endfor %}
    </tbody>
</table>