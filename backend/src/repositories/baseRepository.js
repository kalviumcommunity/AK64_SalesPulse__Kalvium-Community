import { prisma } from '../database/prisma.js';

export class BaseRepository {
  constructor(modelName) {
    this.model = prisma[modelName];
  }

  async findMany(params = {}) {
    return this.model.findMany(params);
  }

  async findUnique(params) {
    return this.model.findUnique(params);
  }

  async findFirst(params) {
    return this.model.findFirst(params);
  }

  async create(params) {
    return this.model.create(params);
  }

  async update(params) {
    return this.model.update(params);
  }

  async delete(params) {
    return this.model.delete(params);
  }

  async count(params = {}) {
    return this.model.count(params);
  }
}

export default BaseRepository;
