import { get } from './global/utils.js';

function chatTemplates(userId, recieverName, message) {
  const currentUserId = localStorage.getItem('userId');

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

$(document).ready(function() {

  const apiBaseUrl = '/api/v1';
  const currentUserId = localStorage.getItem('userId');
  const currentUserName = localStorage.getItem('userName');

  // Connect socket and check if connected success
  const socket = io();
  socket.on('connect', function() {
    console.log('SocketIO connected');
  });

  let receiverId; // Set reciever Id global

  // Handle views for chat section
  $('body').on('click', '.indie-chats', async function() {
    receiverId = $(this).attr('id').split('_')[1];
    const receiver = await get(apiBaseUrl + `/users/${receiverId}`);

    // Unselected all indie-chats class,
    // and select the one click.
    $('.indie-chats').removeClass('selected-nav-group');
    $(this).addClass('selected-nav-group');

    $('#chat-area').empty(); // Clear previous chat
    try {
      const messages = await get(apiBaseUrl + `/receiver/${receiverId}/private-messages`);

      // Clear chat area and append past messages
      //$('#chat-area').empty();
      messages.forEach((msg) => {
        $("#chat-area").append(chatTemplates(msg.sender.sender_id, msg.receiver.username, msg.message.content));
      });
    } catch(error) {
      //$('#chat-area').empty();
      console.log("Error Fetchimg user messages: ", error.responseJSON);
    }
    //console.log(messages);
    $('#chat-box').show();
    $('#chat-title').text(receiver.username);

    // join chat room
    socket.emit('join_chat', { receiver_id: receiverId })
  });

  // Implementation of chat logic
  $('#send__text-icon').click(function() {
    const msg = $('#send-text').text();

    // Ensure that an empty message is not sent
    if (msg) {
      socket.emit('send_message', {
        sender_id: currentUserId,
        receiver_id: receiverId,
        message: msg
      });

      $('#send-text').text('');
    }
  });

  // Event handler for receiving messages
  socket.on('receive_message', function(data) {
    const { sender_id, reciever_id, message, receiver_name } = data;
    $("#chat-area").append(chatTemplates(sender_id, receiver_name, message));
  });
});
