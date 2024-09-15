

async function PrepareRTCConnection() {
    const configuration = {'iceServers': [{'urls': 'stun:stun.l.google.com:19302'}]};
    window.peerConnection = RTCPeerConnection(configuration)
    // Listen for local ICE candidates on the local RTCPeerConnection
    peerConnection.addEventListener('icecandidate', event => {
        if (event.candidate) {
            signalingChannel.send({'new-ice-candidate': event.candidate});
        }
    });

    // Listen for remote ICE candidates and add them to the local RTCPeerConnection
    signalingChannel.addEventListener('message', async message => {
        if (message.iceCandidate) {
            try {
                await peerConnection.addIceCandidate(message.iceCandidate);
            } catch (e) {
                console.error('Error adding received ice candidate', e);
            }
        }
    });
}

async function CreateWebSocket() {
    window.ws = WebSocket()
}

async function RTCOffer() {

}