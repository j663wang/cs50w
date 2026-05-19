document.addEventListener('DOMContentLoaded', function(){

    loadPage(1);
});

async function loadPage(pageNum) {
    fetch(`/posts?page=${pageNum}`)
    .then(response => {
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        renderData(data.posts);
        renderPagination(data.totalPages, pageNum);
    }).catch(error => {
        console.error('Error:', error);
    });
}

function renderData(data) {
    const container = document.querySelector('#posts');
    if (data.length === 0) {
        container.innerHTML = '<p>No posts yet</p>';
        return;
    }
    container.innerHTML = '';  // clear existing   
    data.forEach(post => {
        const postDiv = document.createElement('div');
        postDiv.classList.add('post');
        postDiv.innerHTML = `
            <h3>${post.title}</h3>
            <p>${post.content}</p>
            <small>By ${post.author} on ${new Date(post.timestamp).toLocaleString()}</small>
        `;
        container.appendChild(postDiv);
    });
}


function renderPagination(totalPages, currentPage) {
    const container = document.querySelector('#pagination');
    container.innerHTML = '';  // clear existing

    if (totalPages <= 1) return;  // no pagination needed

    for (let i = 1; i <= totalPages; i++) {
        const btn = document.createElement('button');
        btn.textContent = i;
        btn.classList.toggle('active', i === currentPage);
        btn.addEventListener('click', () => loadPage(i));
        container.appendChild(btn);
    }
}