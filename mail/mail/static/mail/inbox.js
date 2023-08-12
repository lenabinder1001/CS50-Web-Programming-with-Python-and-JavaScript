document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(x, mailid) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#emails-detail-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Reply to mail
  if (mailid !== undefined) {
    fetch(`/emails/${mailid}`)
    .then(response => response.json())
    .then(email => {
      const sender = email.sender;
      const subject = email.subject;
      const body = email.body;
      document.querySelector('#compose-recipients').value = sender;
      if (subject.startsWith('Re:')){
        document.querySelector('#compose-subject').value = subject;
      } else {
        subject_string = 'Re: ' + subject;
        document.querySelector('#compose-subject').value = subject_string;
      }
      body_string = 'On ' + email.timestamp + ' ' + email.sender + ' wrote: ' + body
      document.querySelector('#compose-body').value = body_string;
    });
  }

  // Send mail
  document.querySelector("#compose-form").onsubmit = () => {
    const recipients = document.querySelector("#compose-recipients").value;
    const subject = document.querySelector("#compose-subject").value;
    const body = document.querySelector("#compose-body").value;

    // submit email details via post
    fetch("/network/emails", {
      method: "POST",
      body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body,
      }),
    })
      .then((response) => response.json())
      .then((result) => {
        // Print result
        console.log(result);
        // then load sent mailbox
        load_mailbox("sent");
      });
    return false;
  };
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-detail-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Get mails of requested mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {

    // Create new div for each email
    emails.forEach(element => {

      const mail = document.createElement("div");

      // Styling
      mail.className = 'mail';
      mail.style.border = '1px solid black';
      mail.style.height = '30px'
      mail.style.display = 'flex'
      mail.style.marginBottom = '5px'
      mail.style.cursor = 'pointer'
      
      // Set appropriate backgroundcolor
      if (mailbox == "inbox" || mailbox == "archive") {
        if (element.read == true) {
          mail.style.backgroundColor = 'lightgray'
        }
      }

      // Add different mail contents
      if (mailbox == "sent") {
        // Add email content to div
        mail.innerHTML = `<p style='padding-left: 5px;'><b>${element.recipients}</b></p><p style='padding-left: 5px;'>${element.timestamp}</p><p style='padding-left: 10px;'>${element.body}</p>`;
      } else if (mailbox == "inbox") {
        // Add email content to div
        mail.innerHTML = `<p style='padding-left: 5px;'><b>${element.sender}</b></p><p style='padding-left: 5px;'>${element.timestamp}</p><p style='padding-left: 10px;'>${element.body}</p>`;
      } else if (mailbox == "archive") {
        // Add email content to div
        mail.innerHTML = `<p style='padding-left: 5px;'><b>${element.sender}</b></p><p style='padding-left: 5px;'>${element.timestamp}</p><p style='padding-left: 10px;'>${element.body}</p>`;
      }

      // Add eventListener to show details of each mail
      mail.addEventListener('click', function() {
        fetch(`/emails/${element.id}`, {
          method: 'PUT',
          body: JSON.stringify({
              read: true
          })
        })
        details(mailbox, element.id)
      });

      // Add the newly created element and its content into the DOM
      document.querySelector('#emails-view').append(mail);
    });
  });
}

function details(mailbox, mailid) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-detail-view').style.display = 'block';

  // Set innerHTML to blank to avoid repeating
  document.querySelector("#emails-detail-view").innerHTML = "";

  const mailDetail = document.createElement("div");

  // Styling
  mailDetail.className = 'mailDetail';

  // Get requested mail
  fetch(`/emails/${mailid}`)
  .then(response => response.json())
  .then(email => {
    mailDetail.innerHTML = `<p><b>From: </b>${email.sender}<br><b>To: </b>${email.recipients}<br><b>Subject: </b>${email.subject}<br><b>Timestamp: </b>${email.timestamp}<hr>${email.body}</p>`;
  });

  // Add the newly created element and its content into the DOM
  document.querySelector('#emails-detail-view').append(mailDetail);

  // Create archive and unarchive buttons
  if (mailbox == "inbox") {
    const buttonArchive = document.createElement("button");
    buttonArchive.className = 'archiveButton';
    buttonArchive.innerHTML = 'Archive';

    // Add eventListener to archive mail
    buttonArchive.addEventListener('click', function() {
      fetch(`/emails/${mailid}`, {
        method: 'POST',
        body: JSON.stringify({
            archived: true
        })
      })
      .then(() => {
        load_mailbox("inbox");
      })
    });

    // Add button into the DOM
    document.querySelector('#emails-detail-view').append(buttonArchive);
  }

  if (mailbox == "archive") {
    const buttonUnarchive = document.createElement("button");
    buttonUnarchive.className = 'unarchiveButton';
    buttonUnarchive.innerHTML = 'Unarchive';

    // Add eventListener to archive mail
    buttonUnarchive.addEventListener('click', function() {
      fetch(`/emails/${mailid}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: false
        })
      })
      .then(() => {
        load_mailbox("inbox");
      })
    });

    // Add button into the DOM
    document.querySelector('#emails-detail-view').append(buttonUnarchive);
  }

  if (mailbox == "inbox" || mailbox == "archive"){
    const reply = document.createElement("button");
    reply.className = 'replyButton';
    reply.innerHTML = 'Reply';

    // Add eventListener to reply to mail
    reply.addEventListener('click', function() {
      compose_email("pointerevent", mailid);
    });
    // Add button into the DOM
    document.querySelector('#emails-detail-view').append(reply);
  }
}