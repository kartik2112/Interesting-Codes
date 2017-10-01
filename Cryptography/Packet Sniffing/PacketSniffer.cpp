/**
* To compile this file use
*   g++ PacketSniffer.cpp -lpcap
* Reference: http://www.tcpdump.org/pcap.htm
*/

#include <pcap.h>
#include <iostream>
#include <errno.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>


/* Ethernet protocol ID's */
#define	ETHERTYPE_IP		0x0800		/* IP */
#define	ETHERTYPE_ARP		0x0806		/* ARP */
#define	ETHERTYPE_RARP		0x8035		/* RARP */


/* default snap length (maximum bytes per packet to capture) */
#define SNAP_LEN 1518

/* ethernet headers are always exactly 14 bytes [1] */
#define SIZE_ETHERNET 14

/* Ethernet addresses are 6 bytes */
#define ETHER_ADDR_LEN	6

/* Ethernet header */
struct sniff_ethernet {
        u_char  ether_dhost[ETHER_ADDR_LEN];    /* destination host address */
        u_char  ether_shost[ETHER_ADDR_LEN];    /* source host address */
        u_int16_t ether_type;                     /* IP? ARP? RARP? etc */
};

/* IP header */
struct sniff_ip {
        u_char  ip_vhl;                 /* version << 4 | header length >> 2 */
        u_char  ip_tos;                 /* type of service */
        u_short ip_len;                 /* total length */
        u_short ip_id;                  /* identification */
        u_short ip_off;                 /* fragment offset field */
        #define IP_RF 0x8000            /* reserved fragment flag */
        #define IP_DF 0x4000            /* dont fragment flag */
        #define IP_MF 0x2000            /* more fragments flag */
        #define IP_OFFMASK 0x1fff       /* mask for fragmenting bits */
        u_char  ip_ttl;                 /* time to live */
        u_char  ip_p;                   /* protocol */
        u_short ip_sum;                 /* checksum */
        struct  in_addr ip_src,ip_dst;  /* source and dest address */
};
#define IP_HL(ip)               (((ip)->ip_vhl) & 0x0f)
#define IP_V(ip)                (((ip)->ip_vhl) >> 4)


struct sniff_arp {
		u_int16_t  hType;
		u_int16_t  pType;
		u_short    haLength;
		u_short    paLength;
		char16_t  opcode;
		u_char  senderHA_addr[ETHER_ADDR_LEN];
		struct  in_addr sender_proto;
		u_char  targetHA_addr[ETHER_ADDR_LEN];
		struct  in_addr target_proto;
};


/* TCP header */
typedef u_int tcp_seq;

struct sniff_tcp {
        u_short th_sport;               /* source port */
        u_short th_dport;               /* destination port */
        tcp_seq th_seq;                 /* sequence number */
        tcp_seq th_ack;                 /* acknowledgement number */
        u_char  th_offx2;               /* data offset, rsvd */
#define TH_OFF(th)      (((th)->th_offx2 & 0xf0) >> 4)
        u_char  th_flags;
        #define TH_FIN  0x01
        #define TH_SYN  0x02
        #define TH_RST  0x04
        #define TH_PUSH 0x08
        #define TH_ACK  0x10
        #define TH_URG  0x20
        #define TH_ECE  0x40
        #define TH_CWR  0x80
        #define TH_FLAGS        (TH_FIN|TH_SYN|TH_RST|TH_ACK|TH_URG|TH_ECE|TH_CWR)
        u_short th_win;                 /* window */
        u_short th_sum;                 /* checksum */
        u_short th_urp;                 /* urgent pointer */
};




using namespace std;
//const int BUFSIZ=65535;

void displayPacketContents(u_char *args, const struct pcap_pkthdr *header,const u_char *packet);

int main(int argc, char** argv){
	char errbuf[PCAP_ERRBUF_SIZE];
	char* dev;
	pcap_t *handle;
	struct bpf_program fp;
	bpf_u_int32 mask,net;
	char filter_exp[]="tcp";
	//struct pcap_pkthdr header;
	const u_char *packet;
	
		
	dev=pcap_lookupdev(errbuf);
	
	
	
	if(dev == NULL){
		cout<<"Default Device not found"<<endl;
		return -1;
	}	
	cout<<"Default Device: "<<dev<<endl;
	//cout<<"P1";
	
	if (pcap_lookupnet(dev, &net, &mask, errbuf) == -1) {
		cout<<"Couldn't get netmask for device"<<endl;
		net = 0;
		mask = 0;
	}
	
	handle = pcap_open_live(dev,SNAP_LEN,1,1000,errbuf);
	//cout<<"P2";
	
	if(handle == NULL){
		cout<<"Couldn't open device "<<errbuf<<endl;
		return -1;
	}	
	if (pcap_datalink(handle) != DLT_EN10MB) {
		cout<<"Device doesn't provide Ethernet headers - not supported"<<endl;
		return -1;
	}
	if(pcap_compile(handle,&fp,filter_exp,0,net) == -1){
		cout<<"Couldn't parse filter "<<endl;
		return -1;
	}
	if (pcap_setfilter(handle, &fp) == -1) {
		cout<<"Couldn't apply filter "<<endl;
		return -1;
	}
	
	pcap_loop(handle,30,displayPacketContents,NULL);
	
	//packet=pcap_next(handle,&header);


	//displayPacketContents(packet);
	
	
	pcap_freecode(&fp);
	pcap_close(handle);
	
	return 0;
}

void displayPacketContents(u_char *args, const struct pcap_pkthdr *header,const u_char *packet){
	static int pcktCount=0;
	pcktCount++;
	
	cout<<endl<<endl<<"-----------------------Packet "<<pcktCount<<"----------------------------"<<endl;
	cout<<"  Packet Header Length: "<<header->len<<endl<<endl;
	
	const u_char *ch;
	struct sniff_ethernet *ethernet;
	struct sniff_ip *ip;
	struct sniff_tcp *tcp;
	u_char *payload;
	u_int size_ip;
	u_int size_tcp;
	
	
	ethernet = (struct sniff_ethernet*)(packet);
	
	cout<<"  At Data Link Layer"<<endl;
	
	cout<<"    Source MAC Address: ";
	ch = ethernet->ether_shost;
	for(int i = 0; i < 6; i++){ printf("%02x ", *ch);ch++;}
	cout<<endl;
	
	cout<<"    Destination MAC Address: ";
	ch = ethernet->ether_dhost;
	for(int i = 0; i < 6; i++){ printf("%02x ", *ch);ch++;}
	cout<<endl;
	
	cout<<"    Type: ("<<ethernet->ether_type<<")"<<endl;	
		
	
	if(ethernet->ether_type == 8){
		ip = (struct sniff_ip*)(packet + SIZE_ETHERNET);
		
		cout<<"  IP Packet Header Contents Found:"<<endl;
				
		cout<<"    IP Version: "<<(ip->ip_vhl & 0xf0)<<endl;
		cout<<"    Header Length: "<<(ip->ip_vhl & 0x0f)*4<<endl;
		cout<<"    Type Of Service: ";
		printf("%02x%02x",ip->ip_tos,ip->ip_tos+1);
		cout<<endl;
		cout<<"    Identification: "<<ip->ip_id<<endl;
		cout<<"    Offset: "<<ip->ip_off<<endl;
		cout<<"    TTL: ";
		printf("%02x ", ip->ip_ttl);
		cout<<endl;
		cout<<"    Protocol: ";
		printf("%02x ", ip->ip_p);
		cout<<endl;
		cout<<"    IP Source Address: "<<inet_ntoa(ip->ip_src)<<endl;
		cout<<"    IP Destination Address: "<<inet_ntoa(ip->ip_dst)<<endl;
		
		if(ip->ip_p==0x06){
			size_ip = IP_HL(ip)*4;
			tcp = (struct sniff_tcp*)(packet + SIZE_ETHERNET + size_ip);
			
			cout<<"  TCP Packet Header Contents:"<<endl;
        
        	cout<<"    Source Port:"<<tcp->th_sport<<endl;
        	cout<<"    Destination Port:"<<tcp->th_dport<<endl;
        	cout<<"    Sequence Number:"<<tcp->th_seq<<endl;
        	cout<<"    Acknowledgement Number:"<<tcp->th_ack<<endl;
        	cout<<"    Data Offset:";
        	printf("%02x",tcp->th_offx2);
        	cout<<endl;
        	cout<<"    Window Size:"<<tcp->th_win<<endl;

			size_tcp = TH_OFF(tcp)*4;
			payload = (u_char*)(packet + SIZE_ETHERNET + size_ip + size_tcp);	
			
			ch=payload;
			cout<<"  Payload:"<<endl<<"    ";
			for(int i = 0; i < sizeof(payload); i++){ printf("%02x ", *ch);ch++;}
			cout<<endl;
		}
		
	}
	else if(ethernet->ether_type == 1544){
		cout<<"  ARP Packet Header Contents: "<<endl;
		
		struct sniff_arp *arp=(struct sniff_arp *)(packet + SIZE_ETHERNET-2);
		
		ch = (packet + SIZE_ETHERNET-2);
		for(int i = 0; i < sizeof(arp); i++){ printf("%02x ", *ch);ch++;}
		cout<<endl;
		
		printf("    Hardware Type: %04x\n",arp->hType);
		//printf("    Hardware Type: %d\n",arp->hType);
		printf("    Protocol Type: %04x\n",arp->pType);
		//printf("    Protocol Type: %d\n",arp->pType);
		cout<< "    Hardware Address Length: "<<arp->haLength<<endl;
		cout<< "    Protocol Address Length: "<<arp->paLength<<endl;
		printf("    Opcode: %04x\n",arp->opcode);
		
		cout<< "    Sender Hardware Address: ";
		ch = arp->senderHA_addr;
		for(int i = 0; i < 6; i++){ printf("%02x ", *ch);ch++;}
		cout<<endl;
		
		cout<< "    Sender Protocol Address: "<<inet_ntoa(arp->sender_proto)<<endl;
		
		cout<< "    Target Hardware Address: ";
		ch = arp->targetHA_addr;
		for(int i = 0; i < 6; i++){ printf("%02x ", *ch);ch++;}
		cout<<endl;
		
		cout<< "    Target Protocol Address: "<<inet_ntoa(arp->target_proto)<<endl;
	}
		
}

void displayEntirePacketInHexFormat(const u_char *packet){
	const u_char *ch;
	ch = packet;
	for(int i = 0; i < sizeof(packet); i++){ 
		printf("%02x ", *ch);
		ch++;
		if(i%8==0){
			cout<<endl;
		}
	}
}
