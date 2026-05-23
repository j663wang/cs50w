document.addEventListener('DOMContentLoaded', function(){
    const currentUserId = JSON.parse(document.getElementById('current-user').textContent);
    const isAuthenticated = JSON.parse(document.getElementById('is-authenticated').textContent);
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
        postDiv.setAttribute('data-id', post.id);
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
    if(!isAuthenticated) {
        alert("You must be logged in to edit posts.");
        return;
    }

    if(userId !== currentUserId) {
        alert("You can only edit your own posts.");
        return;
    }
    
    const postDiv = document.querySelector(`div[data-id="${postId}"]`);
    const postContent = document.querySelector(`p[data-id="${postId}"]`);
    const currentContent = postContent.textContent;
    const editBtn = postDiv.querySelector(`.edit-btn[data-id="${postId}"]`);

    // Replace post content with textarea
    const textarea = document.createElement('textarea');
    textarea.value = currentContent;
    postContent.replaceWith(textarea);

    // Change edit button to save button
    const saveBtn = document.createElement('button');
    saveBtn.textContent = 'Save';
    saveBtn.onclick = () => {
        const updatedContent = textarea.value;
        // Send updated content to server
        fetch(`/posts/${postId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ content: updatedContent })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // Update the post content in the UI
            postContent.textContent = updatedContent;
            // Replace the textarea with the updated content
            textarea.replaceWith(postContent);
            // Change the save button back to the edit button
            saveBtn.replaceWith(editBtn);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to update post. Please try again.');
        });
    };
    postDiv.querySelector('.edit-btn').replaceWith(saveBtn);    
}

function likePost(postId) {
    if(!isAuthenticated) {
        alert("You must be logged in to like a post.");
        return;
    }

    fetch(`/likePost/${postId}`,{
        method: 'PATCH',
        headers: {}
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        document.querySelector(`button.like-btn[data-id="${postId}"]`).textContent = `Like (${data.likes})`;
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to like post. Please try again.');
    });
}