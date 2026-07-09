import emailRepository from '../repositories/emailRepository.js';

export class EmailService {
  async analyzeEmail(emailData) {
    return { message: 'analyzeEmail service placeholder' };
  }

  async getEmails() {
    return { message: 'getEmails service placeholder' };
  }
}

export default new EmailService();
