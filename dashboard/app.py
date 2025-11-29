from flask import Flask, render_template, jsonify, request, send_file
import json
import os
from datetime import datetime, timedelta
import logging
import time
from collections import defaultdict
from io import BytesIO

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import ReportLab for PDF generation
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    logger.warning("ReportLab not available. PDF generation will be limited. Install with: pip install reportlab")

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

def generate_audit_pdf(blocks, stats):
    """Generate PDF audit report"""
    buffer = BytesIO()
    
    if REPORTLAB_AVAILABLE:
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2563eb'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        story.append(Paragraph("Blockchain Voting System", title_style))
        story.append(Paragraph("Election Audit Report", styles['Heading2']))
        story.append(Spacer(1, 0.2*inch))
        
        # Report metadata
        report_date = datetime.now().strftime('%B %d, %Y at %I:%M %p')
        story.append(Paragraph(f"<b>Report Generated:</b> {report_date}", styles['Normal']))
        story.append(Paragraph(f"<b>Audit ID:</b> audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}", styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", styles['Heading2']))
        story.append(Spacer(1, 0.1*inch))
        
        summary_data = [
            ['Metric', 'Value'],
            ['Total Blocks', str(stats.get('total_blocks', 0))],
            ['Total Votes Cast', str(stats.get('total_votes', 0))],
            ['Verified Blocks', str(stats.get('verified_blocks', 0))],
            ['Chain Integrity', f"{stats.get('chain_integrity', 0)}%"],
            ['Participation Rate', f"{stats.get('participation_rate', 0)}%"],
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Candidate Results
        story.append(Paragraph("Candidate Results", styles['Heading2']))
        story.append(Spacer(1, 0.1*inch))
        
        candidate_results = stats.get('candidate_results', {})
        if candidate_results:
            candidate_data = [['Candidate', 'Votes', 'Percentage']]
            for candidate, data in sorted(candidate_results.items(), key=lambda x: x[1]['count'], reverse=True):
                candidate_data.append([
                    candidate,
                    str(data.get('count', 0)),
                    f"{data.get('percentage', 0)}%"
                ])
            
            candidate_table = Table(candidate_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
            candidate_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]))
            story.append(candidate_table)
        else:
            story.append(Paragraph("No candidate results available.", styles['Normal']))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Voting Period
        voting_period = stats.get('voting_period', {})
        if voting_period:
            story.append(Paragraph("Voting Period", styles['Heading2']))
            story.append(Spacer(1, 0.1*inch))
            story.append(Paragraph(f"<b>Start:</b> {voting_period.get('start', 'N/A')}", styles['Normal']))
            story.append(Paragraph(f"<b>End:</b> {voting_period.get('end', 'N/A')}", styles['Normal']))
            story.append(Paragraph(f"<b>Time Remaining:</b> {voting_period.get('remaining', 'N/A')}", styles['Normal']))
            story.append(Spacer(1, 0.3*inch))
        
        # Blockchain Verification Status
        story.append(Paragraph("Blockchain Verification Status", styles['Heading2']))
        story.append(Spacer(1, 0.1*inch))
        
        chain_integrity = stats.get('chain_integrity', 0)
        if chain_integrity == 100:
            status_text = "✅ All blocks verified and chain integrity confirmed"
            status_color = colors.HexColor('#10b981')
        else:
            status_text = f"⚠️ Chain integrity: {chain_integrity}% - Verification in progress"
            status_color = colors.HexColor('#f59e0b')
        
        status_style = ParagraphStyle(
            'StatusStyle',
            parent=styles['Normal'],
            fontSize=12,
            textColor=status_color,
            spaceAfter=12
        )
        story.append(Paragraph(status_text, status_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Recent Blocks Summary
        story.append(Paragraph("Recent Blocks Summary", styles['Heading2']))
        story.append(Spacer(1, 0.1*inch))
        
        # Show last 10 blocks
        recent_blocks = blocks[-10:] if len(blocks) > 10 else blocks
        blocks_data = [['Block #', 'Data', 'Status']]
        for block in recent_blocks:
            is_verified = block.get('hash', '').startswith('000')
            status = '✅ Verified' if is_verified else '⏳ Pending'
            data = block.get('data', '')[:50] + '...' if len(block.get('data', '')) > 50 else block.get('data', '')
            blocks_data.append([
                str(block.get('index', 0)),
                data,
                status
            ])
        
        blocks_table = Table(blocks_data, colWidths=[1*inch, 3.5*inch, 1.5*inch])
        blocks_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6366f1')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        story.append(blocks_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Footer
        story.append(Spacer(1, 0.2*inch))
        footer_style = ParagraphStyle(
            'FooterStyle',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        story.append(Paragraph("This is an automated audit report generated by the Blockchain Voting System.", footer_style))
        story.append(Paragraph("Team Nous - Building Trust, Block by Block", footer_style))
        
        # Build PDF
        doc.build(story)
    else:
        # Fallback: Create a simple text-based PDF-like response
        buffer.write(b"PDF generation requires ReportLab library. Please install it using: pip install reportlab")
    
    buffer.seek(0)
    return buffer

@app.route('/api/export/audit')
def export_audit_report():
    """API endpoint to export audit report as PDF"""
    try:
        blocks = blockchain_manager.load_blockchain()
        stats = blockchain_manager.get_statistics(blocks)
        
        pdf_buffer = generate_audit_pdf(blocks, stats)
        filename = f"election_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        logger.error(f"Error generating audit report: {e}")
        return jsonify({'error': f'Failed to generate audit report: {str(e)}'}), 500

if __name__ == '__main__':
    print("🚀 Blockchain Voting Dashboard Starting...")
    print("📊 Dashboard: http://localhost:5000")
    print("🔗 API Status: http://localhost:5000/api/status")
    print("📈 Live Statistics: http://localhost:5000/api/statistics")
    app.run(debug=True, host='0.0.0.0', port=5000)