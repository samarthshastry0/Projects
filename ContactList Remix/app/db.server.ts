import { readFileSync, writeFileSync, existsSync } from "fs";
import { join } from "path";

const dbPath = join(process.cwd(), "contacts.json");

export interface Contact {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
}

export interface ContactInput {
  first_name: string;
  last_name: string;
  email: string;
}

interface Database {
  contacts: Contact[];
  nextId: number;
}

function initDb(): Database {
  if (!existsSync(dbPath)) {
    const initialData: Database = { contacts: [], nextId: 1 };
    writeFileSync(dbPath, JSON.stringify(initialData, null, 2));
    return initialData;
  }
  return JSON.parse(readFileSync(dbPath, "utf-8"));
}

function saveDb(data: Database): void {
  writeFileSync(dbPath, JSON.stringify(data, null, 2));
}

export function getContacts(): Contact[] {
  const db = initDb();
  return db.contacts.sort((a, b) => b.id - a.id);
}

export function getContact(id: number): Contact | undefined {
  const db = initDb();
  return db.contacts.find((c) => c.id === id);
}

export function createContact(contact: ContactInput): Contact {
  const db = initDb();
  
  if (db.contacts.some((c) => c.email === contact.email)) {
    throw new Error("Email already exists");
  }
  
  const newContact: Contact = {
    id: db.nextId++,
    ...contact,
  };
  
  db.contacts.push(newContact);
  saveDb(db);
  return newContact;
}

export function updateContact(id: number, contact: ContactInput): boolean {
  const db = initDb();
  const index = db.contacts.findIndex((c) => c.id === id);
  
  if (index === -1) return false;
  
  if (db.contacts.some((c) => c.id !== id && c.email === contact.email)) {
    throw new Error("Email already exists");
  }
  
  db.contacts[index] = { id, ...contact };
  saveDb(db);
  return true;
}

export function deleteContact(id: number): boolean {
  const db = initDb();
  const initialLength = db.contacts.length;
  db.contacts = db.contacts.filter((c) => c.id !== id);
  
  if (db.contacts.length < initialLength) {
    saveDb(db);
    return true;
  }
  return false;
}
