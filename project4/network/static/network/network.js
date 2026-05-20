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
        postDiv.classList.add('postContainer');
        postDiv.innerHTML = `
            <h3 data-id="${post.id}">${post.title}</h3>
            <button class ="edit-btn" data-id="${post.id}">Edit</button>
            <p data-id="${post.id}">${post.content}</p>
            <small>By ${post.author} on ${new Date(post.timestamp).toLocaleString()}</small>
            <button class="like-btn" data-id="${post.id}">Like (${post.likes})</button>
        `;
        container.appendChild(postDiv);

        // Add event listeners for like and edit buttons
        postDiv.querySelector('.edit-btn').addEventListener('click', () => editPost(post.id, post.userId));
        postDiv.querySelector('.like-btn').addEventListener('click', () => likePost(post.id));
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

function editPost(postId, userId) {
    if(userId !== currentUserId) {
        alert("You can only edit your own posts.");
        return;
    }
    
    const postContent = document.querySelector(`p[data-id="${postId}"]`);

    
    
}

function likePost(){

}