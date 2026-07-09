document.addEventListener('DOMContentLoaded', () => {
    const commentContainer = document.querySelector('#comment-container');
    const username = commentContainer.dataset.username;
    const default_page = 1;
    loadComments(username,default_page);
    if(document.querySelector('#follow-toggle')){
        const followToggle = document.querySelector('#follow-toggle');
    }
});

function loadComments(username, page=1) {
    fetch(`/social/comments/${username}/?page=${page}`)
    .then(response => response.json())
    .then(data => {
        renderComments(data.comments);
        renderPagination(data.current_page,data.total_page, username);
    })
};

function renderComments(comments){
    const commentList = document.querySelector('#comment-list');
    commentList.innerHTML = '';
    comments.forEach(comment=> {
        const div = document.createElement('div')
        div.className = 'comment-item';
        div.innerHTML = `
            <strong>${comment.username}</strong>
            <small>${comment.created_at}</small>
            <p>${comment.content}</p>
        `;
        commentList.appendChild(div);
    })
};

function renderPagination(current_page, total_page, username){
    const pagination = document.querySelector('#pagination');
    pagination.innerHTML = '';
    for(let i=1; i<=total_page; i++){
        const button = document.createElement('button');
        button.textContent = i;
        button.className = i === current_page ? 'active' : '';
        button.addEventListener('click', () => {
            loadComments(username, i);
        });
        pagination.appendChild(button);
    }
};   
