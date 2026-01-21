import { json, redirect, type ActionFunctionArgs, type LoaderFunctionArgs } from "@remix-run/node";
import { useLoaderData, Form, useNavigation } from "@remix-run/react";
import { getContacts, createContact, updateContact, deleteContact, type Contact } from "../db.server";
import { useState } from "react";

export async function loader({ request }: LoaderFunctionArgs) {
  const contacts = getContacts();
  return json({ contacts });
}

export async function action({ request }: ActionFunctionArgs) {
  const formData = await request.formData();
  const intent = formData.get("intent");

  try {
    switch (intent) {
      case "create": {
        const firstName = formData.get("firstName") as string;
        const lastName = formData.get("lastName") as string;
        const email = formData.get("email") as string;

        if (!firstName || !lastName || !email) {
          return json({ error: "All fields are required" }, { status: 400 });
        }

        createContact({
          first_name: firstName,
          last_name: lastName,
          email,
        });
        return redirect("/?success=created");
      }

      case "update": {
        const id = parseInt(formData.get("id") as string);
        const firstName = formData.get("firstName") as string;
        const lastName = formData.get("lastName") as string;
        const email = formData.get("email") as string;

        if (!firstName || !lastName || !email) {
          return json({ error: "All fields are required" }, { status: 400 });
        }

        updateContact(id, {
          first_name: firstName,
          last_name: lastName,
          email,
        });
        return redirect("/?success=updated");
      }

      case "delete": {
        const id = parseInt(formData.get("id") as string);
        deleteContact(id);
        return redirect("/?success=deleted");
      }

      default:
        return json({ error: "Invalid intent" }, { status: 400 });
    }
  } catch (error) {
    return json({ error: "An error occurred. Email might already exist." }, { status: 500 });
  }
}

export default function Index() {
  const { contacts } = useLoaderData<typeof loader>();
  const navigation = useNavigation();
  const [editingContact, setEditingContact] = useState<Contact | null>(null);

  const isSubmitting = navigation.state === "submitting";

  return (
    <div className="container">
      <h1>Contact List</h1>

      <div className="card">
        <h2>{editingContact ? "Update Contact" : "Add New Contact"}</h2>
        <Form method="post" key={editingContact?.id || "new"}>
          <input
            type="hidden"
            name="intent"
            value={editingContact ? "update" : "create"}
          />
          {editingContact && (
            <input type="hidden" name="id" value={editingContact.id} />
          )}

          <div className="form-group">
            <label htmlFor="firstName">First Name:</label>
            <input
              type="text"
              id="firstName"
              name="firstName"
              defaultValue={editingContact?.first_name || ""}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="lastName">Last Name:</label>
            <input
              type="text"
              id="lastName"
              name="lastName"
              defaultValue={editingContact?.last_name || ""}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="email">Email:</label>
            <input
              type="email"
              id="email"
              name="email"
              defaultValue={editingContact?.email || ""}
              required
            />
          </div>

          <div className="button-group">
            <button type="submit" disabled={isSubmitting}>
              {isSubmitting
                ? "Saving..."
                : editingContact
                ? "Update Contact"
                : "Add Contact"}
            </button>
            {editingContact && (
              <button
                type="button"
                onClick={() => setEditingContact(null)}
              >
                Cancel
              </button>
            )}
          </div>
        </Form>
      </div>

      <div className="card">
        <h2>Contacts</h2>
        {contacts.length === 0 ? (
          <div className="empty-state">
            No contacts yet. Add your first contact above!
          </div>
        ) : (
          <div className="contacts-list">
            {contacts.map((contact) => (
              <div key={contact.id} className="contact-item">
                <div className="contact-info">
                  <h3>
                    {contact.first_name} {contact.last_name}
                  </h3>
                  <p>{contact.email}</p>
                </div>
                <div className="contact-actions">
                  <button
                    className="btn-update"
                    onClick={() => setEditingContact(contact)}
                  >
                    Update
                  </button>
                  <Form method="post" style={{ display: "inline" }}>
                    <input type="hidden" name="intent" value="delete" />
                    <input type="hidden" name="id" value={contact.id} />
                    <button
                      type="submit"
                      className="btn-delete"
                      onClick={(e) => {
                        if (!confirm("Are you sure you want to delete this contact?")) {
                          e.preventDefault();
                        }
                      }}
                    >
                      Delete
                    </button>
                  </Form>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
