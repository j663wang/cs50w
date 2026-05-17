document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(recipients = '', subject = '', body = '') {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_email(email_id) {
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Fetch the email details
  fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(email => {
      // Display the email details
      const emailView = document.querySelector('#emails-view');
      emailView.innerHTML = `
        <div class="email-header">
        <h3>${email.subject}</h3>
        <p><strong>From:</strong> ${email.sender}</p>
        <p><strong>To:</strong> ${email.recipients.join(', ')}</p>
        <p><strong>Timestamp:</strong> ${email.timestamp}</p>
        </div>
        <hr>
        <div class="email-body">
        <p>${email.body}</p>
        </div>
      `;

      const emailHeader = emailView.querySelector('.email-header');

      // create the reply button and add to email header
      const replyButton = document.createElement('button');
      replyButton.textContent = 'Reply';
      replyButton.addEventListener('click', () => {
        compose_email(email.sender, email.subject, email.body);
      });
      emailHeader.appendChild(replyButton);

      // create the archive/unarchive button and add to email header
      const archiveButton = document.createElement('button');
      archiveButton.textContent = email.archived ? 'Unarchive' : 'Archive';
      archiveButton.addEventListener('click', () => {
        fetch(`/emails/${email_id}`, {
          method: 'PUT',
          body: JSON.stringify({
            archived: !email.archived
          })
        }).then(() => load_mailbox('inbox'));
      });
      emailHeader.appendChild(archiveButton);

      // Mark the email as read if it's not already
      if (!email.read) {
        fetch(`/emails/${email_id}`, {
          method: 'PUT',
          body: JSON.stringify({
            read: true
          })
        });
      }
    }).catch(error => console.error('Error:', error));

}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Clear the emails view
  const emailsView = document.querySelector('#emails-view');
  emailsView.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {

      // if there are no emails, display a message
      if (emails.length === 0) {
        emailsView.innerHTML += '<p>No emails to display.</p>';
      } else {
        // Loop through each email and create a div for it
        emails.forEach(email => {
          const emailDiv = document.createElement('div');
          emailDiv.className = 'email-item';
          emailDiv.innerHTML = `
            <strong>${mailbox === 'sent' ? email.recipients.join(', ') : email.sender}</strong>
            <span>${email.subject}</span>
            <span>${email.timestamp}</span>
          `;

          // Add click event to load the email details
          emailDiv.addEventListener('click', () => load_email(email.id));

          // Append the email div to the emails view
          emailsView.appendChild(emailDiv);
        });
      }
    } ).catch(error => console.error('Error:', error));

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}