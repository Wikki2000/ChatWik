import { get, getBaseUrl } from '../global/utils.js';

function chatTemplates(userId, recieverName, message) {
  const currentUserId = localStorage.getItem('userId');
  const API_BASE_URL = getBaseUrl()['apiBaseUrl'];

  if (currentUserId === userId) {
    return `<div class="chat-bubble sent">
      <p class="client-display-name">Me</p>
      <p class="sent-message">${message}</p>
    </div>`;
  }

  return `<div class="chat-bubble received">
    <p class="sender-display-name">${recieverName}</p>
    <p class="received-message">${message}</p>
  </div>`;
}

function friendSectionTemplate(
  userData, timeStamp = 'Just now',
  acceptBottonContent = 'Add',
  rejectButtonContent = 'Cancel'
) {
  return `<li class="chat-list">
    <a href="#">
      <div class="chat-list-image online">
        <img src="/static/images/profile_photo_placeholder.jpeg" alt="Profile Photo" class="dashboard__user-avatar">
      </div>

      <div class="chat-details">
        <h4 id="name" class="name">${userData.username}</h4>
        <p class="accept__reject-btns">
           <button data-id="${userData.id}" class="btn btn-success">${acceptBottonContent}</button>
           <button data-id="${userData.id}"class="btn btn-danger reject">${rejectButtonContent}</button>
         </p>
       </div>

       <div class="content">
         <h6 class="content-timestamp">${timeStamp}</h6>
       </div>
     </a>
   </li>
  `
}
$(document).ready(function() {

  const apiBaseUrl = '/api/v1';
  const currentUserId = localStorage.getItem('userId');
  const recieverId = $('#user-data').data('friend_id');

  async function getFriendData() {
    const url = apiBaseUrl + `/users/${recieverId}`;
    try {
      const friendData = await get(url);
      const chatStatus = friendData.is_active ? 'on-line' : 'off-line';
      $('#dynamic__chat-title').text(friendData.username);
      $('#dynamic__chat-status').text(chatStatus);
    } catch(err) {
      console.log(err);
    }
  }
  getFriendData();

  // Connect socket and check if connected success
  const socket = io();
  socket.on('connect', function() {
    console.log('SocketIO connected');
  });

  // Go back to previous page
  $('.fa-chevron-left').click(function() {
    window.history.back();
  });

  async function loadChat() {
    try {

      const url = apiBaseUrl + `/messages/${recieverId}/private-messages`;
      const messages = await get(url);
      messages.forEach(({ message, reciever, sender }) => {
        $("#chat-area").append(
          chatTemplates(sender.sender_id, sender.username, message.content)
        );
	      console.log(reciever.username, sender.username)
      });
    } catch(error) {
      console.log(error);
    }
  }
  loadChat();

  // Join the user and his friend in  room for private chat
  socket.emit('join_chat', { reciever_id: recieverId })

  // Make Send icon visible when input field not empty.
  $('#send-text').on('input', function() {
    if ($('#send-text').val()) {
      $('#send__text-icon').css('opacity', 1);
    } else {
      $('#send__text-icon').css('opacity', 0.5);
    }
  });

  // Handle sending of message to friend
  $('#send__text-icon').click(function() {
    const msg = $('#send-text').val();

    // Ensure that an empty message is not sent
    if (msg) {
      socket.emit('send_message', {
        reciever_id: recieverId,
        message: msg
      });

      $('#send-text').val('');
    }
  });

  // Event handler for receiving messages
  socket.on('recieve_message', function(data) {
    const { sender_id, reciever_id, message, sender_name } = data;
    $("#chat-area").append(chatTemplates(sender_id, sender_name, message));
  });
});
