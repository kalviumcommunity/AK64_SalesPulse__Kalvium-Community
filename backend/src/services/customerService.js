import customerRepository from '../repositories/customerRepository.js';

export class CustomerService {
  async createCustomer(customerData) {
    return { message: 'createCustomer service placeholder' };
  }

  async getCustomers() {
    return { message: 'getCustomers service placeholder' };
  }
}

export default new CustomerService();
