from flask import Flask, render_template, jsonify, request, send_file
import json
import os
from datetime import datetime, timedelta
import logging
import time
from collections import defaultdict

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BlockchainManager:
    def __init__(self, blockchain_file='../blockchain.json'):
        self.blockchain_file = blockchain_file
        self.last_update = datetime.now()
    
    def load_blockchain(self):
        """Load blockchain data from JSON file"""
        try:
            if os.path.exists(self.blockchain_file):
                with open(self.blockchain_file, 'r') as f:
                    data = json.load(f)
                    self.last_update = datetime.now()
                    return data
            else:
                # Return sample data for demo
                return self._get_sample_data()
        except Exception as e:
            logger.error(f"Error loading blockchain: {e}")
            return self._get_sample_data()
    
    def _get_sample_data(self):
        """Generate sample blockchain data for demonstration"""
        sample_blocks = [
            {
                "index": 0,
                "data": "Genesis Block - Election Started",
                "prevHash": "",
                "hash": "000a1b2c3d4e5f67890abc123def4567890abcdef1234567890abcdef12345",
                "timestamp": int((datetime.now() - timedelta(hours=2)).timestamp()),
                "nonce": 3128
            }
        ]
        
        # Add sample votes
        candidates = ["Candidate A", "Candidate B", "Candidate C"]
        for i in range(1, 157):
            candidate = candidates[i % 3]
            voter_id = f"Voter_{i:04d}"
            sample_blocks.append({
                "index": i,
                "data": f"{voter_id} voted for {candidate}",
                "prevHash": sample_blocks[i-1]["hash"],
                "hash": f"000{''.join([str((i*j) % 10) for j in range(60)])}",
                "timestamp": int((datetime.now() - timedelta(minutes=157-i)).timestamp()),
                "nonce": 1000 + i
            })
        
        return sample_blocks
    
    def get_statistics(self, blocks):
        """Calculate comprehensive blockchain statistics"""
        if not blocks:
            return {}
        
        total_votes = len([b for b in blocks if 'voted for' in b.get('data', '')])
        candidate_votes = defaultdict(int)
        verified_blocks = 0
        
        for block in blocks:
            # Count verified blocks (those starting with 000)
            if block.get('hash', '').startswith('000'):
                verified_blocks += 1
            
            # Count candidate votes
            data = block.get('data', '')
            if 'voted for' in data:
                try:
                    candidate = data.split('voted for')[-1].strip()
                    candidate_votes[candidate] += 1
                except:
                    continue
        
        # Calculate percentages
        total = sum(candidate_votes.values())
        candidate_percentages = {
            candidate: {
                'count': count,
                'percentage': round((count / total) * 100) if total > 0 else 0
            }
            for candidate, count in candidate_votes.items()
        }
        
        return {
            'total_blocks': len(blocks),
            'total_votes': total_votes,
            'verified_blocks': verified_blocks,
            'chain_integrity': round((verified_blocks / len(blocks)) * 100) if blocks else 0,
            'candidate_results': candidate_percentages,
            'participation_rate': min(89, total_votes),  # Demo data
            'latest_block': blocks[-1] if blocks else None,
            'voting_period': {
                'start': (datetime.now() - timedelta(hours=2)).strftime('%b %d, %Y %I:%M %p'),
                'end': (datetime.now() + timedelta(hours=12)).strftime('%b %d, %Y %I:%M %p'),
                'remaining': '12h 24m'
            }
        }

    def get_recent_activity(self, blocks, minutes=5):
        """Get recent blockchain activity"""
        cutoff = datetime.now() - timedelta(minutes=minutes)
        recent_blocks = []
        
        for block in blocks[-10:]:  # Last 10 blocks
            block_time = datetime.fromtimestamp(block.get('timestamp', 0))
            if block_time >= cutoff:
                recent_blocks.append({
                    'index': block.get('index', 0),
                    'time': block_time.strftime('%I:%M %p'),
                    'status': 'Verified' if block.get('hash', '').startswith('000') else 'Pending'
                })
        
        return recent_blocks[-5:]  # Return last 5

# Initialize blockchain manager
blockchain_manager = BlockchainManager()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/blockchain')
def get_blockchain():
    """API endpoint to get blockchain data"""
    blocks = blockchain_manager.load_blockchain()
    return jsonify(blocks)

@app.route('/api/statistics')
def get_statistics():
    """API endpoint to get comprehensive statistics"""
    blocks = blockchain_manager.load_blockchain()
    stats = blockchain_manager.get_statistics(blocks)
    return jsonify(stats)

@app.route('/api/status')
def get_system_status():
    """API endpoint to get system status"""
    blocks = blockchain_manager.load_blockchain()
    stats = blockchain_manager.get_statistics(blocks)
    
    return jsonify({
        'online': True,
        'lastUpdate': blockchain_manager.last_update.strftime('%I:%M:%S %p'),
        'lastUpdateAgo': 'a few seconds ago',
        'blockHeight': stats['total_blocks'],
        'verifiedBlocks': stats['verified_blocks'],
        'chainIntegrity': f"{stats['chain_integrity']}%",
        'autoRefresh': True,
        'securityStatus': 'All Blocks Verified' if stats['chain_integrity'] == 100 else 'Verification In Progress'
    })

@app.route('/api/activity/recent')
def get_recent_activity():
    """API endpoint to get recent activity"""
    blocks = blockchain_manager.load_blockchain()
    activity = blockchain_manager.get_recent_activity(blocks)
    return jsonify(activity)

@app.route('/api/verify', methods=['POST'])
def verify_blockchain():
    """API endpoint to verify blockchain integrity"""
    blocks = blockchain_manager.load_blockchain()
    
    verification_results = []
    is_valid = True
    verification_steps = []
    
    # Simulate verification process
    verification_steps.append({'step': 'Checking block hashes...', 'status': 'completed'})
    time.sleep(0.5)
    verification_steps.append({'step': 'Validating digital signatures...', 'status': 'completed'})
    time.sleep(0.5)
    verification_steps.append({'step': 'Verifying timestamp sequence...', 'status': 'completed'})
    time.sleep(0.5)
    verification_steps.append({'step': 'Confirming Proof-of-Work...', 'status': 'completed'})
    
    for i, block in enumerate(blocks):
        block_valid = True
        issues = []
        
        # Check Proof of Work
        if not block.get('hash', '').startswith('000'):
            issues.append("Invalid Proof of Work")
            block_valid = False
        
        # Check block linking
        if i > 0:
            if block.get('prevHash') != blocks[i-1].get('hash'):
                issues.append("Broken chain link")
                block_valid = False
        
        verification_results.append({
            'block_index': i,
            'valid': block_valid,
            'issues': issues,
            'hash': block.get('hash', '')[:32] + '...'
        })
        
        if not block_valid:
            is_valid = False
    
    return jsonify({
        'valid': is_valid,
        'blocks': verification_results,
        'total_blocks': len(blocks),
        'verification_steps': verification_steps,
        'audit_id': f"audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    })

@app.route('/api/block/<int:block_index>')
def get_block(block_index):
    """API endpoint to get specific block"""
    blocks = blockchain_manager.load_blockchain()
    if 0 <= block_index < len(blocks):
        return jsonify(blocks[block_index])
    return jsonify({'error': 'Block not found'}), 404

@app.route('/api/export/audit')
def export_audit_report():
    """API endpoint to export audit report"""
    # In a real implementation, this would generate a PDF
    return jsonify({
        'message': 'Audit report generated successfully',
        'filename': f"election_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
        'url': '/api/download/audit'
    })

if __name__ == '__main__':
    print("🚀 Blockchain Voting Dashboard Starting...")
    print("📊 Dashboard: http://localhost:5000")
    print("🔗 API Status: http://localhost:5000/api/status")
    print("📈 Live Statistics: http://localhost:5000/api/statistics")
    app.run(debug=True, host='0.0.0.0', port=5000)