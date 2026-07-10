import { BaseRepository } from './baseRepository.js';

export class CustomerRepository extends BaseRepository {
  constructor() {
    super('customer');
  }
}

export default new CustomerRepository();
